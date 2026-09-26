# vim: set ts=4 sw=4 et: coding=UTF-8

import logging
import os.path
import re
from http.client import HTTPException
from urllib import parse
from urllib.request import Request, urlopen

import pyrpm.spec  # type: ignore

from .dependency_parser import DependencyParser, DepParserError
from .rpmexception import NoMatchExceptionError
from .rpmhelpers import fix_license
from .rpmpreambleelements import MacroLine, RpmPreambleElements
from .rpmrequirestoken import RpmRequiresToken
from .rpmsection import Section

logger = logging.getLogger('RpmPreamble')
# Switch to logging.DEBUG if needed. FIXME: Add debug flag to the command line options
logger.setLevel(logging.ERROR)


class RpmPreamble(Section):
    """
    A class providing methods for preamble section cleaning.

        Only keep one empty line for many consecutive ones.
        Reorder lines.
        Fix bad licenses.
        Use one line per BuildRequires/Requires/etc.
        Standardize BuildRoot.

        This one is a bit tricky since we reorder things. We have a notion of
        paragraphs, categories, and groups.

        A paragraph is a list of non-empty lines. Conditional directives like
        %if/%else/%endif also mark paragraphs. It contains categories.
        A category is a list of lines on the same topic. It contains a list of
        groups.
        A group is a list of lines where the first few ones are comment lines,
        and the last one is a normal line.

        This means that comments will stay attached to one
        line, even if we reorder the lines.
    """

    def __init__(self, options):
        """Initialize all the global variables and known categories."""
        Section.__init__(self, options)
        # Old storage
        self._oldstore = []
        # Is the parsed variable multiline (ending with \)
        # alternatively if the line contains %{expand while the ending } is on other line
        self.multiline = False
        self.multiline_expand = False
        # Open { braces of the multiline %{expand: block
        self._expand_depth = 0
        # Is the multiline macro a %global, expanded while parsing
        self._multiline_global = False
        # Are we inside of conditional or not
        self.condition = False
        # Does the %if/%elif condition continue on the next line (ending with \)
        self._condition_continued = False
        # Is the condition with define/global variables
        self._condition_define = False
        # Is the condition based probably on bcond evaluation
        self._condition_bcond = False
        # Stack for _condition_bcond to prevent nested blocks from
        # contaminating outer blocks.
        self._bcond_stack = []
        # Stack for _condition_define so a nested bcond/define block does
        # not leak the flag to sibling blocks (only parents inherit it).
        self._define_stack = []
        # Is the condition based on the pattern
        self._pattern_condition = False
        # Does the condition hold Name/Version/Release/Epoch tags
        self._condition_nvr = False
        # How many multi-line %{?cond: ... } blocks are currently open, so we
        # know a lone } closes such a block instead of being misc content
        self._multilinecond_depth = 0
        self.options = options
        # do we want pkgconfig and others?
        self.pkgconfig = options['pkgconfig']
        self.perl = options['perl']
        self.cmake = options['cmake']
        self.tex = options['tex']
        # are we supposed to keep empty lines intact?
        self.keep_space = options['keep_space']
        # do we want to remove groups from the specfile?
        self.remove_groups = options['remove_groups']
        # dict of license replacement options
        self.license_conversions = options['license_conversions']
        # dict of pkgconfig and other conversions
        self.pkgconfig_conversions = options['pkgconfig_conversions']
        self.perl_conversions = options['perl_conversions']
        self.cmake_conversions = options['cmake_conversions']
        self.tex_conversions = options['tex_conversions']
        # list of allowed groups
        self.allowed_groups = options['allowed_groups']
        # start the object
        self.paragraph = RpmPreambleElements(options)
        # license handling
        self.subpkglicense = options['subpkglicense']
        # License seen at any nesting level, so no placeholder is needed
        self._has_license = False
        # modname detection
        self.modname = None
        # comments separated from a removed tag by a blank line are kept
        self._comments_before_blank = 0

        # simple categories matching
        # missing categories have a special match in add() method (comments explain what and why is missing there)
        self.category_to_re = {
            'name': self.reg.re_name,
            'version': self.reg.re_version,
            'epoch': self.reg.re_epoch,
            # license need fix replacment
            'summary': self.reg.re_summary,
            # for url we have a special match - http -> https replacement
            'group': self.reg.re_group,
            'nosource': self.reg.re_nosource,
            # for source, we have a special match to keep the source number
            # for patch, we have a special match to keep the patch number
            'buildsystem': self.reg.re_buildsystem,
            'buildoption': self.reg.re_buildoption,
            'buildrequires': self.reg.re_buildrequires,
            'buildconflicts': self.reg.re_buildconflicts,
            'buildignores': self.reg.re_buildignores,
            'conflicts': self.reg.re_conflicts,
            # for prereq we append warning comment so we don't mess it there
            # requires has a special match - pwdutils -> shadow replacement
            'recommends': self.reg.re_recommends,
            'suggests': self.reg.re_suggests,
            'enhances': self.reg.re_enhances,
            'supplements': self.reg.re_supplements,
            # for provides/obsoletes, we have a special case because we group them
            # for build root, we have a special match because we force its value
            'removepath': self.reg.re_removepath,
            'buildarch': self.reg.re_buildarch,
            'excludearch': self.reg.re_excludearch,
            'exclusivearch': self.reg.re_exclusivearch,
            'tail': self.reg.re_tail_macros,
            'head': self.reg.re_head_macros,
        }

        # deprecated definitions that we no longer want to see
        self.category_to_clean = {
            'vendor': self.reg.re_vendor,
            'autoreqprov': self.reg.re_autoreqprov,
            'icon': self.reg.re_icon,
            'copyright': self.reg.re_copyright,
            'packager': self.reg.re_packager,
            'debugpkg': self.reg.re_debugpkg,
            'prefix': self.reg.re_preamble_prefix,
            'buildroot': self.reg.re_buildroot,
            'py_requires': self.reg.re_py_requires,
        }

    def start_subparagraph(self):
        """Backup the paragraph and start a new one."""
        self._oldstore.append(self.paragraph)
        self.paragraph = RpmPreambleElements(self.options)

    def _prune_ppc_condition(self):
        """Check if we have ppc64 obsolete and delete it."""
        if (
            not self.minimal
            and len(self.paragraph.items['conditions']) == 3
            and isinstance(self.paragraph.items['conditions'][0], list)
            and self.paragraph.items['conditions'][0][0] == '# bug437293'
            and self.paragraph.items['conditions'][1].endswith('64bit')
        ):
            self.paragraph.items['conditions'] = []

    def _prune_empty_condition(self):
        """Remove empty conditions."""
        conditions = self.paragraph.items['conditions']
        # check if we have just the if (maybe with comments) and its endif
        if len(conditions) == 2:
            opener = conditions[0][-1] if isinstance(conditions[0], list) else conditions[0]
            if opener.startswith('%if') and self.reg.re_endif.match(conditions[1]):
                self.paragraph.items['conditions'] = []

    PYPI_SOURCE_HOSTS = ('pypi.io', 'files.pythonhosted.org', 'pypi.python.org')

    def _fix_pypi_source(self, url):
        """
        Check if the source is URL that points to PyPI.

        If it is, return the canonical version.

        This function is almost completely self-contained and only processes
        the URL structure itself. On PyPI, the structure is predictable.
        The only bad thing that can happen is the packager choosing to use
        a macro instead of an explicit name of the file.
        (which doesn't really make much sense, given that the url contains
        the first letter of the name, so that is going to be explicit anyway)
        """
        parsed = parse.urlparse(url)
        # not an URL
        if not parsed.scheme:
            return url

        # not pypi location
        if parsed.netloc not in self.PYPI_SOURCE_HOSTS:
            return url

        # hashed download url, its first directory is not a package type
        if self.reg.re_pypi_hashed.match(parsed.path):
            return url

        if self.reg.re_pypi_type.match(parsed.path):
            match = self.reg.re_pypi_type.match(parsed.path)
            pkg_type = match.group('type')
        else:
            pkg_type = 'source'

        filename = os.path.basename(parsed.path)
        if self.reg.re_pypi_modname.match(filename):
            match = self.reg.re_pypi_modname.match(filename)
            modname = match.group('pkgname')
        else:
            # no modname -> can't compile url
            return url

        # TODO the following condition checks if the name contains a macro,
        # and expects that if it does, the macro is called "modname". This is not
        # always the case. It would be better to detect the name of the macro and
        # browse local definitions to find its value.
        if '%' in modname:
            if (modname == '%modname' or modname == '%{modname}') and self.modname:
                modname = self.modname
            else:
                # don't know what to do
                return url
        return parse.urlunparse(
            (
                'https',
                'files.pythonhosted.org',
                f'/packages/{pkg_type}/{modname[0]}/{modname}/{filename}',
                parsed.params,
                parsed.query,
                parsed.fragment,
            )
        )

    def _place_define_condition(self, sub_has_bconds, sub_has_defines):
        """
        Place a conditional block that defines macros.

        The destination is determined solely by the block's content, not by
        the parent's state, so placement is stable across passes.

        - Bcond tests (%if %{with foo}) go to bcond_conditions: they must stay
          below the bcond definitions, otherwise the switches have no effect.
        - Blocks defining only bconds (no %define) go with bcond definitions.
        - Blocks with %defines (possibly mixed with bconds) go with defines.
        """
        if self._condition_bcond:
            # Bcond test: must stay below bcond definitions.
            self.paragraph.items['bcond_conditions'] += self.paragraph.items['conditions']
        elif sub_has_bconds and not sub_has_defines:
            # Only bconds, no defines: with the bcond definitions.
            self.paragraph.items['bconds'] += self.paragraph.items['conditions']
        else:
            # Has defines: with the define definitions.
            self.paragraph.add_define_block(self.paragraph.items['conditions'])

    def end_subparagraph(self, endif=False, unclosed=False):
        """
        End the paragraph and flatten the output.

        If we are at the end we need to flatten and sort everything and give it
        in the layers to the paragraph above us. A block still open at the
        next section header goes after everything else, as its %endif follows
        that section.
        """
        if not self._oldstore:
            nested = False
        else:
            nested = True
        if any(self.paragraph.items[i] for i in ('name', 'version', 'release', 'epoch')):
            self._condition_nvr = True
        # Track whether the sub block defines bconds (for placement).
        # This is based on the sub's content, not the parent's state.
        # (read before flattening, which moves late defines out of 'define')
        sub_has_bconds = len(self.paragraph.items['bconds']) > 0
        sub_has_defines = len(self.paragraph.items['define']) > 0
        if sub_has_defines or sub_has_bconds:
            self._condition_define = True
        lines = self.paragraph.flatten_output(False, nested)
        self.paragraph = self._oldstore.pop(-1)
        self.paragraph.items['conditions'] += lines

        if unclosed:
            self.paragraph.items['open_conditions'] += self.paragraph.items['conditions']
            self.paragraph.items['conditions'] = []
            return

        # If we are on endif we check the condition content
        # and if we find the defines we put it on top.
        if endif or not self.condition:
            self._prune_empty_condition()
            self._prune_ppc_condition()
            if self._condition_define:
                # in source order; _split_late_globals moves it below the tags or bconds it reads
                if (
                    self._condition_bcond
                    or self.paragraph.has_late_globals(self.paragraph.items['conditions'])
                    or (
                        sub_has_bconds
                        and self.paragraph.reads_moved_macros(self.paragraph.items['conditions'])
                    )
                ):
                    self.paragraph.add_define_block(self.paragraph.items['conditions'])
                else:
                    self._place_define_condition(sub_has_bconds, sub_has_defines)
            else:
                # the tags define %name/%version/..., which the later tags expand
                if self._condition_nvr and self.paragraph.reads_late_macros(
                    self.paragraph.items['conditions']
                ):
                    # in source order; _split_late_globals keeps it below the globals it reads
                    self.paragraph.add_define_block(self.paragraph.items['conditions'])
                elif self._condition_nvr:
                    self.paragraph.items['nvr_conditions'] += self.paragraph.items['conditions']
                elif self._pattern_condition:
                    self.paragraph.items['patterncodeblock'] += self.paragraph.items['conditions']
                else:
                    self.paragraph.items['build_conditions'] += self.paragraph.items['conditions']

            # Restore the outer block's bcond flag from the stack.
            # This prevents nested bcond conditionals from contaminating
            # the placement of outer blocks.
            if self._bcond_stack:
                self._condition_bcond = self._bcond_stack.pop()
            # Restore the outer block's define flag, keeping the "contains
            # defines" bit so parents of a nested bcond/define block still
            # move to the top; siblings start fresh instead of inheriting it.
            if self._define_stack:
                self._condition_define = self._define_stack.pop() or self._condition_define
            # top-level reset
            if len(self._oldstore) == 0:
                self._condition_bcond = False
                self._bcond_stack = []
                self._condition_define = False
                self._define_stack = []
                self._pattern_condition = False
                self._condition_nvr = False
            self.paragraph.items['conditions'] = []

    @staticmethod
    def _pkgname_to_brackety(token, brackety, conversions):
        converted = []
        # just never convert pkgconfig dependency
        # The same if we do not have a match
        if token.name == 'pkgconfig' or token.name not in conversions:
            return token
        else:
            # first split the data
            convers_list = conversions[token.name].split()
            # then add each pkgconfig to the list
            # print pkgconf_list
            for j in convers_list:
                name = f'{brackety}({j})'
                converted.append(RpmRequiresToken(name, token.operator, token.version))
        return converted

    @staticmethod
    def _split_trailing_comment(value):
        # Separate trailing %dnl or # comments before dependency parsing.
        # They are not part of the dependency and would crash the parser.
        trailing_comment = None
        dnl_idx = value.find('%dnl')
        if dnl_idx >= 0:
            trailing_comment = value[dnl_idx:].strip()
            value = value[:dnl_idx].strip()
        else:
            hash_idx = -1
            for i, ch in enumerate(value):
                if ch == '#':
                    if i == 0 or value[i - 1] in ' \t':
                        hash_idx = i
                        break
            if hash_idx >= 0:
                trailing_comment = value[hash_idx:].strip()
                value = value[:hash_idx].strip()
        return value, trailing_comment

    @staticmethod
    def _attach_trailing_comment(tokens, trailing_comment):
        if not trailing_comment or not tokens:
            return
        # flat_out() only yields RpmRequiresToken items, so the comment
        # belongs to the last token on the line
        tokens[-1].trailing_comment = trailing_comment

    def _fix_list_of_packages(self, value, category):
        # we do fix the package list only if there is no rpm call there on line
        # otherwise print there warning about nicer content and skip
        if self.reg.re_rpm_command.search(value):
            if (
                category == 'requires'
                and not (self.previous_line and self.previous_line.startswith('#'))
                and not self.minimal
            ):
                self.paragraph.current_group.append('# FIXME: Use %requires_eq macro instead')
            return [value]
        dependencies, trailing_comment = self._split_trailing_comment(value)
        try:
            tokens = DependencyParser(dependencies).flat_out()
        except (DepParserError, NoMatchExceptionError):
            # keep a value we cannot parse as it is instead of crashing on it
            return [value]
        self._attach_trailing_comment(tokens, trailing_comment)
        # loop over all and do formatting as we can get more deps for one
        expanded = []
        for token in tokens:
            # skip all various rpm-macroed content as it
            # is usually not easy to determine how that should be
            # split
            if token.name.startswith('%'):
                expanded.append(token)
                continue
            # scriptlet deps and package names (Provides/Obsoletes, %requires_eq/ge) stay as is
            if category not in (
                'prereq',
                'requires_phase',
                'provides_obsoletes',
                'requires_eq',
                'requires_ge',
            ):
                # here we go with descending priority to find match and replace
                # the strings by some optimistic value of brackety dep
                # priority is based on the first come first serve
                if self.pkgconfig:
                    token = self._pkgname_to_brackety(
                        token, 'pkgconfig', self.pkgconfig_conversions
                    )
                # checking if it is not list is simple avoidance of running
                # over already converted values
                if not isinstance(token, list) and self.perl:
                    token = self._pkgname_to_brackety(token, 'perl', self.perl_conversions)
                if not isinstance(token, list) and self.tex:
                    token = self._pkgname_to_brackety(token, 'tex', self.tex_conversions)
                if not isinstance(token, list) and self.cmake:
                    token = self._pkgname_to_brackety(token, 'cmake', self.cmake_conversions)
            if isinstance(token, list):
                expanded += token
            else:
                expanded.append(token)
        return expanded

    def _add_line_value_to(self, category, value, key=None):
        """
        Change a key-value line, to make sure we have the right spacing.

        Note: since we don't have a key <-> category matching, we need to
        redo one. (Eg: Provides and Obsoletes are in the same category)
        """
        key = self.paragraph.compile_category_prefix(category, key)

        if category in self.paragraph.categories_with_package_tokens:
            values = self._fix_list_of_packages(value, category)
            for value in values:
                if isinstance(value, str):
                    value = key + value
                else:
                    value.prefix = key
                self._add_line_to(category, value)
        else:
            line = key + value
            self._add_line_to(category, line)

    def _add_line_to(self, category, line):
        # Tail macros (e.g. %python_subpackages) inside a conditional
        # must stay with their %if/%endif wrapper. Routing them to
        # 'conditions' keeps the block atomic; otherwise the macro escapes
        # to the top-level tail and the output is not idempotent.
        # Head macros already sort before the %endif and must stay above the tags.
        if category == 'tail' and self.condition:
            category = 'conditions'
        group = line
        if self.paragraph.current_group:
            if isinstance(line, RpmRequiresToken):
                line.comments = self.paragraph.current_group
            else:
                self.paragraph.current_group.append(line)
                group = self.paragraph.current_group
            self.paragraph.current_group = []
            self._comments_before_blank = 0
        # each define entry is a unit, which moves as a whole
        self.paragraph.items[category].append([group] if category == 'define' else group)

        self.previous_line = str(line)

    def _drop_pending_comments(self):
        """Drop the comments written directly above a tag that is removed."""
        del self.paragraph.current_group[self._comments_before_blank :]

    def _make_secure_url(self, orig_url, skip_availabilty_check=False, force_https=False):
        retval = None
        secure_url = None
        if parse.urlparse(orig_url).scheme == '' and force_https:
            secure_url = 'https://' + orig_url
        elif orig_url.startswith('http://'):
            secure_url = orig_url.replace('http', 'https', 1)
        elif orig_url.startswith('ftp://'):
            # Try to convert it to https, some sites support this
            secure_url = orig_url.replace('ftp', 'https', 1)
        if skip_availabilty_check:
            return secure_url if secure_url else orig_url

        response = None
        try:
            if secure_url and not self.minimal:
                req = Request(url=secure_url, headers={'User-Agent': 'Mozilla/5.0'})
                response = urlopen(req, timeout=5)
                retval = secure_url if response.getcode() == 200 else orig_url
            else:
                retval = orig_url
        # best-effort probe: network, http.client and url encoding errors keep the original url
        except (OSError, HTTPException, ValueError):
            retval = orig_url
        finally:
            if response:
                response.close()
        return retval

    def _macro_line(self, line):
        """Tag a %define, %global or one-line condition line with when rpm expands it."""
        oneline = bool(self.reg.re_onelinecond.match(line))
        is_global = bool(self.reg.re_global.match(line)) or (oneline and '%global' in line)
        # a one-line condition is evaluated when parsed, even around %define
        return MacroLine(line, is_global=is_global, is_eager=is_global or oneline)

    def add(self, line):
        """Run over options and add the determined line to proper location."""
        # a } ending a line also closes a %{?cond: block; split it off so sorting keeps it last
        content = line.rstrip()
        if (
            self._multilinecond_depth > 0
            and not (self.multiline or self._condition_continued)
            and content.endswith('}')
            and content.count('}') > content.count('{')
            and content[:-1].strip()
        ):
            RpmPreamble.add(self, content[:-1])
            RpmPreamble.add(self, '}')
            return
        line = self._complete_cleanup(line)

        if self.condition and self.reg.re_patternmacro.search(line):
            self._pattern_condition = True

        # the continued condition stays right after its %if/%elif line
        if self._condition_continued:
            self._condition_continued = line.endswith('\\')
            line = MacroLine(line, is_cond=True, is_eager=True)
            self._oldstore[-1].items['conditions'].append(line)
            if '%{with' in line or '%{without' in line:
                self._condition_bcond = True
            self.previous_line = line
            return

        # if it is multiline variable then we need to append to previous content
        # also multiline is allowed only for define lines so just cheat and
        # know ahead
        if self.multiline:
            line = MacroLine(
                line, is_global=self._multiline_global, is_eager=self._multiline_global
            )
            self.paragraph.items['define'][-1].append(line)
            self.previous_line = line
            # if it is no longer trailed with backslash
            # or if the braces of the expand are balanced then stop
            if self.multiline_expand:
                self._expand_depth += line.count('{') - line.count('}')
                if self._expand_depth <= 0:
                    self.multiline_expand = False
                    self.multiline = False
            else:
                if not line.endswith('\\'):
                    self.multiline = False
            return

        # if the line is empty, just skip it, unless keep_space is true
        elif not self.keep_space and len(line) == 0:
            self._comments_before_blank = len(self.paragraph.current_group)
            return

        # If we match the if else or endif we create subgroup
        # this is basically our class again until we match
        # else where we mark end of paragraph or endif
        # which mark the end of our subclass and that we can
        # return the data to our main class for at-bottom placement
        elif self.reg.re_if.match(line) or self.reg.re_codeblock.match(line):
            self._add_line_to('conditions', MacroLine(line, is_cond=True, is_eager=True))
            self.condition = True
            self._condition_continued = line.endswith('\\')
            # save the outer block's flag before setting this block's own
            self._bcond_stack.append(self._condition_bcond)
            # save the outer block's define flag and start this block fresh;
            # a nested bcond/define block must not leak the flag to the
            # sibling blocks parsed after it, only parents inherit it
            self._define_stack.append(self._condition_define)
            self._condition_define = False
            # check for possibility of the bcond conditional
            # Reset for each new block; the flag is sticky otherwise and
            # contaminates subsequent non-bcond conditionals.
            if '%{with' in line or '%{without' in line:
                self._condition_bcond = True
            else:
                self._condition_bcond = False
            self.start_subparagraph()
            self.previous_line = line
            return

        elif self.reg.re_else_elif.match(line):
            if self.condition:
                self._add_line_to('conditions', MacroLine(line, is_cond=True, is_eager=True))
                self.end_subparagraph()
                self.start_subparagraph()
                self._condition_continued = line.endswith('\\')
            self.previous_line = line
            return

        elif self.reg.re_multilinecond.match(line):
            # Multi-line %{?cond: block is an abbreviated %if cond block,
            # parse it as a condition so the dependencies inside keep it.
            self._add_line_to('conditions', MacroLine(line, is_cond=True, is_eager=True))
            self.condition = True
            self._multilinecond_depth += 1
            # the block keeps the outer block's flag, restored at its closing brace
            self._bcond_stack.append(self._condition_bcond)
            self._define_stack.append(self._condition_define)
            self._condition_define = False
            self.start_subparagraph()
            self.previous_line = line
            return

        elif (
            self.reg.re_endif.match(line)
            or self.reg.re_endcodeblock.match(line)
            or (self._multilinecond_depth > 0 and self.reg.re_endmultilinecond.match(line))
        ):
            # A lone } closes a multi-line %{?cond: block.
            if self.reg.re_endmultilinecond.match(line):
                self._multilinecond_depth -= 1
            self._add_line_to('conditions', line)
            # Set conditions to false only if we are
            # closing last of the nested ones
            if len(self._oldstore) == 1:
                self.condition = False
            self.end_subparagraph(True)
            self.previous_line = line
            return

        elif self.reg.re_comment.match(line) and not self.reg.re_buildignores.match(line):
            if line or self.previous_line:
                self.paragraph.current_group.append(line)
                self.previous_line = line
            if not line:
                self._comments_before_blank = len(self.paragraph.current_group)
            return

        # replace 'http' with 'https' in URL if https is reachable (#246)
        elif self.reg.re_url.match(line):
            match = self.reg.re_url.match(line)
            secure_url = self._make_secure_url(match.group(1), force_https=True)
            self._add_line_value_to('url', secure_url, key='URL')
            return

        elif self.reg.re_source.match(line):
            match = self.reg.re_source.match(line)
            source = match.group(2)
            secure_source_available = False

            # expand the spec file to get URLs that can be checked
            # (best-effort: pyrpm chokes on some valid spec files)
            try:
                # parse the spec once per run, not once per Source line
                if 'pyrpm_spec' not in self.options:
                    self.options['pyrpm_spec'] = pyrpm.spec.Spec.from_file(self.options['specfile'])
                spec = self.options['pyrpm_spec']
                # expand the cleaned value, spec.sources holds the raw (not curlified) text
                expanded_source_url = pyrpm.spec.replace_macros(source, spec)
                if self._make_secure_url(expanded_source_url) != expanded_source_url:
                    secure_source_available = True
            except Exception:
                # On pyrpm failure, continue with normal Source handling;
                # only the HTTPS availability enhancement is skipped.
                pass

            if not self.minimal:
                source = self._fix_pypi_source(source)
                if secure_source_available:
                    source = self._make_secure_url(source, skip_availabilty_check=True)
            self._add_line_value_to('source', source, key=f'Source{match.group(1)}')
            return

        elif self.reg.re_patch.match(line):
            match = self.reg.re_patch.match(line)
            number = match.group(2)
            # %prep applies the bare %patch as '%patch -P 0'
            if not number and not match.group(1) and self.options['rename_unnumbered_patch']:
                number = '0'
                self.options['rename_unnumbered_patch'] = False
            self._add_line_value_to(
                'patch',
                match.group(3),
                key=f'{match.group(1)}Patch{number}',
            )
            return

        elif self.reg.re_buildoption_phase.match(line):
            match = self.reg.re_buildoption_phase.match(line)
            value = match.group(2)
            self._add_line_value_to('buildoption_phase', value, key=f'BuildOption{match.group(1)}')
            return

        elif self.reg.re_bcond_with.match(line):
            self._add_line_to('bconds', line)
            return

        elif self.reg.re_mingw.match(line):
            self._add_line_to('define', line)
            return

        elif self.reg.re_patterndefine.match(line):
            self._add_line_to('define', line)
            return

        elif self.reg.re_provides.match(line) and self.reg.re_patternmacro.search(line):
            match = self.reg.re_provides.match(line)
            self._add_line_value_to('patternprovides', match.group(1), key='Provides')
            return

        elif self.reg.re_provides.match(line) and self.reg.re_patternobsolete.search(line):
            match = self.reg.re_provides.match(line)
            self._add_line_value_to('patternobsoletes', match.group(1), key='Provides')
            return

        elif self.reg.re_requires.match(line) and self.reg.re_patternmacro.search(line):
            match = self.reg.re_requires.match(line)
            self._add_line_value_to('patternrequires', match.group(1), key='Requires')
            return

        elif self.reg.re_recommends.match(line) and self.reg.re_patternmacro.search(line):
            match = self.reg.re_recommends.match(line)
            self._add_line_value_to('patternrecommends', match.group(1), key='Recommends')
            return

        elif self.reg.re_suggests.match(line) and self.reg.re_patternmacro.search(line):
            match = self.reg.re_suggests.match(line)
            self._add_line_value_to('patternsuggests', match.group(1), key='Suggests')
            return

        elif self.reg.re_obsoletes.match(line) and self.reg.re_patternobsolete.search(line):
            match = self.reg.re_obsoletes.match(line)
            self._add_line_value_to('patternobsoletes', match.group(1), key='Obsoletes')
            return

        elif self.reg.re_requires_eq.match(line):
            match = self.reg.re_requires_eq.match(line)
            if match.group(1):
                # if we were wrapped in curly definiton we need to remove
                # the trailing curly bracket
                value = match.group(2)[:-1]
            else:
                value = match.group(2)
            self._add_line_value_to('requires_eq', value)
            return

        elif self.reg.re_requires_ge.match(line):
            match = self.reg.re_requires_ge.match(line)
            if match.group(1):
                # if we were wrapped in curly definiton we need to remove
                # the trailing curly bracket
                value = match.group(2)[:-1]
            else:
                value = match.group(2)
            self._add_line_value_to('requires_ge', value)
            return

        elif self.reg.re_onelinecond_dep.match(line):
            # One-line conditional dependency (%{?cond:BuildRequires: ...}) is
            # an abbreviated %if cond ... %endif block, keep it with the
            # other conditions instead of the defines at the top.
            self._add_line_to('build_conditions', self._macro_line(line))
            return

        elif (
            self.reg.re_define.match(line)
            or self.reg.re_global.match(line)
            or self.reg.re_onelinecond.match(line)
        ):
            line = self._macro_line(line)
            self._multiline_global = line.is_global
            if line.endswith('\\'):
                self.multiline = True
            open_braces = line.count('{') - line.count('}')
            if '%{expand:' in line and open_braces > 0:
                self.multiline = True
                self.multiline_expand = True
                self._expand_depth = open_braces
            # if we are kernel and not multiline we need to be at bottom, so
            # lets use misc section, otherwise go for define
            if not self.multiline and line.find('kernel_module') >= 0:
                self._add_line_to('misc', line)
            else:
                self._add_line_to('define', line)

            # catch "modname" for use in pypi url rewriting
            match = self.reg.re_modname_define.match(line)
            if match:
                # a macro value cannot be put into the url path
                self.modname = None if match.group(1).startswith('%') else match.group(1)

            return

        elif self.reg.re_prereq.match(line):
            match = self.reg.re_prereq.match(line)
            self._add_line_value_to('prereq', match.group(1))
            return

        # replace pwdutils with shadow in Requires (#247)
        elif self.reg.re_requires.match(line):
            match = self.reg.re_requires.match(line)
            if match.group(1) == 'pwdutils' and not self.condition and not self.minimal:
                value = 'shadow'
            else:
                value = match.group(1)
            self._add_line_value_to('requires', value, key='Requires')
            return

        # replace pwdutils with shadow in Requires(phase) (#247)
        elif self.reg.re_requires_phase.match(line):
            match = self.reg.re_requires_phase.match(line)
            # Put the requires content properly as key for formatting
            if match.group(2) == 'pwdutils' and not self.condition and not self.minimal:
                value = 'shadow'
            else:
                value = match.group(2)
            self._add_line_value_to('requires_phase', value, key=f'Requires{match.group(1)}')
            return

        elif self.reg.re_provides.match(line):
            match = self.reg.re_provides.match(line)
            self._add_line_value_to('provides_obsoletes', match.group(1), key='Provides')
            return

        elif self.reg.re_obsoletes.match(line):
            match = self.reg.re_obsoletes.match(line)
            self._add_line_value_to('provides_obsoletes', match.group(1), key='Obsoletes')
            return

        elif self.reg.re_license.match(line):
            # first convert the license string to proper format and then append
            match = self.reg.re_license.match(line)
            value = match.groups()[len(match.groups()) - 1]
            value = fix_license(value, self.license_conversions)
            self._has_license = True
            # only store subpkgs if they have different licenses
            if not (type(self).__name__ == 'RpmPackage' and not self.subpkglicense):
                self._add_line_value_to('license', value)
            else:
                self._drop_pending_comments()
            return

        elif self.reg.re_release.match(line):
            match = self.reg.re_release.match(line)
            value = match.group(1)
            if re.search(r'[a-zA-Z\s]', value):
                self._add_line_value_to('release', value)
            else:
                self._add_line_value_to('release', '0')
            return

        elif self.reg.re_summary_localized.match(line):
            match = self.reg.re_summary_localized.match(line)
            # we need to know what language we need
            language = match.group(1)
            # and what value is there
            content = match.group(2)
            self._add_line_value_to('summary_localized', content, key=f'Summary{language}')
            return

        elif self.reg.re_group.match(line):
            # remove groups if requested
            if not self.minimal and self.remove_groups:
                self._drop_pending_comments()
                return

            # validate (if we have a list of groups)
            match = self.reg.re_group.match(line)
            value = match.group(1)
            if not self.minimal and self.allowed_groups:
                if (
                    self.previous_line
                    and not self.previous_line.startswith('# FIXME')
                    and value not in self.allowed_groups
                ):
                    self.paragraph.current_group.append(
                        '# FIXME: use correct group or remove it,'
                        ' see "https://en.opensuse.org/openSUSE:Package_group_guidelines"'
                    )
            self._add_line_value_to('group', value)
            return

        elif self.reg.re_buildarch.match(line):
            match = self.reg.re_buildarch.match(line)
            value = match.group(2)
            if value.startswith('noarch'):
                self._add_line_value_to('buildarch', value)
            else:
                self._add_line_value_to('exclusivearch', value)

        elif self.reg.re_head_macros.match(line):
            self._add_line_value_to('head', line)

        # loop for all other matching categories which
        # do not require special attention
        else:
            # cleanup
            for _category, regexp in self.category_to_clean.items():
                match = regexp.match(line)
                if match:
                    self._drop_pending_comments()
                    return

            # simple matching
            for category, regexp in self.category_to_re.items():
                match = regexp.match(line)
                if match:
                    # instead of matching first group as there is only one,
                    # take the last group (including "whole match" if no groups present)
                    # (so I can have more advanced regexp for RPM tags)
                    self._add_line_value_to(category, match.group(len(match.groups())))
                    return

            self._add_line_to('misc', line)

    def output(self, fout, newline=True, new_class=None):
        """Dump the results to the output list."""
        lines = self.paragraph.flatten_output(self.subpkglicense and not self._has_license)
        self.lines += lines
        Section.output(self, fout, newline, new_class)


class RpmPreambleChunk(RpmPreamble):
    """Preamble lines (%define, %global, %bcond) between sections, not a package header."""

    def output(self, fout, newline=True, new_class=None):
        """Dump the results to the output list without a placeholder License."""
        self.lines += self.paragraph.flatten_output(False)
        Section.output(self, fout, newline, new_class)
