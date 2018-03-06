# vim: set ts=4 sw=4 et: coding=UTF-8

import os.path
import re

try:
    from urllib import parse as urlparse
except ImportError:
    import urlparse

from .rpmsection import Section
from .rpmpreambleelements import RpmPreambleElements
from .dependency_parser import DependencyParser
from .rpmhelpers import fix_license
from .rpmrequirestoken import RpmRequiresToken


class RpmPreamble(Section):

    """
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
        Section.__init__(self, options)
        # Old storage
        self._oldstore = []
        # Is the parsed variable multiline (ending with \)
        self.multiline = False
        # Are we inside of conditional or not
        self.condition = False
        # Is the condition with define/global variables
        self._condition_define = False
        # Is the condition based probably on bcond evaluation
        self._condition_bcond = False
        # Is the condition based on the pattern
        self._pattern_condition = False
        self.options = options
        # do we want pkgconfig and others?
        self.pkgconfig = options['pkgconfig']
        self.perl = options['perl']
        self.cmake = options['cmake']
        self.tex = options['tex']
        # are we supposed to keep empty lines intact?
        self.keep_space = options['keep_space']
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
        # modname detection
        self.modname = None

        # simple categories matching
        self.category_to_re = {
            'name': self.reg.re_name,
            'version': self.reg.re_version,
            # license need fix replacment
            'summary': self.reg.re_summary,
            'url': self.reg.re_url,
            'group': self.reg.re_group,
            'nosource': self.reg.re_nosource,
            # for source, we have a special match to keep the source number
            # for patch, we have a special match to keep the patch number
            'buildrequires': self.reg.re_buildrequires,
            'buildconflicts': self.reg.re_buildconflicts,
            'buildignores': self.reg.re_buildignores,
            'conflicts': self.reg.re_conflicts,
            # for prereq we append warning comment so we don't mess it there
            'requires': self.reg.re_requires,
            'recommends': self.reg.re_recommends,
            'suggests': self.reg.re_suggests,
            'enhances': self.reg.re_enhances,
            'supplements': self.reg.re_supplements,
            # for provides/obsoletes, we have a special case because we group them
            # for build root, we have a special match because we force its value
            'buildarch': self.reg.re_buildarch,
            'excludearch': self.reg.re_excludearch,
            'exclusivearch': self.reg.re_exclusivearch,
            'tail': self.reg.re_tail_macros,
        }

        # deprecated definitions that we no longer want to see
        self.category_to_clean = {
            'vendor': self.reg.re_vendor,
            'autoreqprov': self.reg.re_autoreqprov,
            'epoch': self.reg.re_epoch,
            'icon': self.reg.re_icon,
            'copyright': self.reg.re_copyright,
            'packager': self.reg.re_packager,
            'debugpkg': self.reg.re_debugpkg,
            'prefix': self.reg.re_preamble_prefix,
            'buildroot': self.reg.re_buildroot,
            'py_requires': self.reg.re_py_requires,
        }

    def start_subparagraph(self):
        # Backup the list and start a new one
        self._oldstore.append(self.paragraph)
        self.paragraph = RpmPreambleElements(self.options)

    def _prune_ppc_condition(self):
        """
        Check if we have ppc64 obsolete and delete it
        """
        if not self.minimal and \
                len(self.paragraph.items['conditions']) == 3 and \
                isinstance(self.paragraph.items['conditions'][0], list) and \
                self.paragraph.items['conditions'][0][0] == '# bug437293' and \
                self.paragraph.items['conditions'][1].endswith('64bit'):
            self.paragraph.items['conditions'] = []

    def _prune_empty_condition(self):
        """
        Remove empty conditions
        """
        # check if we start with if
        if len(self.paragraph.items['conditions']) == 2 and \
                ((isinstance(self.paragraph.items['conditions'][0], list) and \
                self.paragraph.items['conditions'][0][-1].startswith("%if")) or \
                self.paragraph.items['conditions'][0].startswith("%if")):
            self.paragraph.items['conditions'] = []

    PYPI_SOURCE_HOSTS = ("pypi.io", "files.pythonhosted.org", "pypi.python.org")

    def _fix_pypi_source(self, url):
        """
        Check if the source is URL that points to PyPI and if it is, return
        the canonical version.

        This function is almost completely self-contained and only processes
        the URL structure itself. On PyPI, the structure is predictable.
        The only bad thing that can happen is the packager choosing to use
        a macro instead of an explicit name of the file.
        (which doesn't really make much sense, given that the url contains
        the first letter of the name, so that is going to be explicit anyway)
        """
        parsed = urlparse.urlparse(url)
        # not an URL
        if not parsed.scheme:
            return url

        # not pypi location
        if parsed.netloc not in self.PYPI_SOURCE_HOSTS:
            return url

        filename = os.path.basename(parsed.path)
        modname = filename[:filename.rfind("-")]

        # TODO the following condition checks if the filename starts with a macro,
        # and expects that if it does, the macro is called "modname". This is not
        # always the case. It would be better to detect the name of the macro and
        # browse local definitions to find its value.
        if modname[0] == "%":
            if (modname == "%modname" or modname == "%{modname}") \
                    and self.modname:
                modname = self.modname
            else:
                # don't know what to do
                return url

        return urlparse.urlunparse(('https', 'files.pythonhosted.org', '/packages/source/{}/{}/{}'.format(modname[0], modname, filename), '', '', ''))

    def end_subparagraph(self, endif=False):
        if not self._oldstore:
            nested = False
        else:
            nested = True
        lines = self.paragraph.flatten_output(False, nested)
        if len(self.paragraph.items['define']) > 0 or \
           len(self.paragraph.items['bconds']) > 0:
            self._condition_define = True
        self.paragraph = self._oldstore.pop(-1)
        self.paragraph.items['conditions'] += lines

        # If we are on endif we check the condition content
        # and if we find the defines we put it on top.
        if endif or not self.condition:
            self._prune_empty_condition()
            self._prune_ppc_condition()
            if self._condition_define:
                # If we have define conditions and possible bcond start
                # we need to put it bellow bcond definitions as otherwise
                # the switches do not have any effect
                if self._condition_bcond:
                    self.paragraph.items['bcond_conditions'] += self.paragraph.items['conditions']
                elif len(self.paragraph.items['define']) == 0:
                    self.paragraph.items['bconds'] += self.paragraph.items['conditions']
                else:
                    self.paragraph.items['define'] += self.paragraph.items['conditions']
                # in case the nested condition contains define we consider all parents
                # to require to be on top too;
                if len(self._oldstore) == 0:
                    self._condition_define = False
            else:
                if self._pattern_condition:
                    self.paragraph.items['patterncodeblock'] += self.paragraph.items['conditions']
                else:
                    self.paragraph.items['build_conditions'] += self.paragraph.items['conditions']

            # bcond must be reseted when on top and can be set even outside of the
            # define scope. So reset it here always
            if len(self._oldstore) == 0:
                self._condition_bcond = False
                self._pattern_condition = False
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
                name = '{0}({1})'.format(brackety, j)
                converted.append(RpmRequiresToken(name, token.operator, token.version))
        return converted

    def _fix_list_of_packages(self, value, category):
        # we do fix the package list only if there is no rpm call there on line
        # otherwise print there warning about nicer content and skip
        if self.reg.re_rpm_command.search(value):
            if category == 'requires' and not self.previous_line.startswith('#') and not self.minimal:
                self.paragraph.current_group.append('# FIXME: Use %requires_eq macro instead')
            return [value]
        tokens = DependencyParser(value).flat_out()
        # loop over all and do formatting as we can get more deps for one
        expanded = []
        for token in tokens:
            # skip all various rpm-macroed content as it
            # is usually not easy to determine how that should be
            # split
            if token.name.startswith('%'):
                expanded.append(token)
                continue
            # in scriptlets we most probably do not want the converted deps
            if category != 'prereq' and category != 'requires_phase':
                # here we go with descending priority to find match and replace
                # the strings by some optimistic value of brackety dep
                # priority is based on the first come first serve
                if self.pkgconfig:
                    token = self._pkgname_to_brackety(token, 'pkgconfig', self.pkgconfig_conversions)
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
        if self.paragraph.current_group:
            if isinstance(line, RpmRequiresToken):
                line.comments = self.paragraph.current_group
                self.paragraph.items[category].append(line)
            else:
                self.paragraph.current_group.append(line)
                self.paragraph.items[category].append(self.paragraph.current_group)
            self.paragraph.current_group = []
        else:
            self.paragraph.items[category].append(line)

        self.previous_line = str(line)

    def add(self, line):
        line = self._complete_cleanup(line)

        if self.condition and self.reg.re_patternmacro.search(line):
            self._pattern_condition = True

        # if the line is empty, just skip it, unless keep_space is true
        if not self.keep_space and len(line) == 0:
            return

        # if it is multiline variable then we need to append to previous content
        # also multiline is allowed only for define lines so just cheat and
        # know ahead
        elif self.multiline:
            self._add_line_to('define', line)
            # if it is no longer trailed with backslash stop
            if not line.endswith('\\'):
                self.multiline = False
            return

        # If we match the if else or endif we create subgroup
        # this is basically our class again until we match
        # else where we mark end of paragraph or endif
        # which mark the end of our subclass and that we can
        # return the data to our main class for at-bottom placement
        elif self.reg.re_if.match(line) or self.reg.re_codeblock.match(line):
            self._add_line_to('conditions', line)
            self.condition = True
            # check for possibility of the bcond conditional
            if "%{with" in line or "%{without" in line:
                self._condition_bcond = True
            self.start_subparagraph()
            self.previous_line = line
            return

        elif self.reg.re_else.match(line):
            if self.condition:
                self._add_line_to('conditions', line)
                self.end_subparagraph()
                self.start_subparagraph()
            self.previous_line = line
            return

        elif self.reg.re_endif.match(line) or self.reg.re_endcodeblock.match(line):
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
            return

        elif self.reg.re_source.match(line):
            match = self.reg.re_source.match(line)
            source = match.group(2)
            if not self.minimal:
                source = self._fix_pypi_source(source)
            self._add_line_value_to('source', source, key='Source%s' % match.group(1))
            return

        elif self.reg.re_patch.match(line):
            match = self.reg.re_patch.match(line)
            # convert Patch: to Patch0:
            if match.group(2) == '':
                zero = '0'
            else:
                zero = ''
            self._add_line_value_to('patch', match.group(3), key='%sPatch%s%s' % (match.group(1), zero, match.group(2)))
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

        elif self.reg.re_define.match(line) or self.reg.re_global.match(line) or self.reg.re_onelinecond.match(line):
            if line.endswith('\\'):
                self.multiline = True
            # if we are kernel and not multiline we need to be at bottom, so
            # lets use misc section, otherwise go for define
            if not self.multiline and line.find("kernel_module") >= 0:
                self._add_line_to('misc', line)
            else:
                self._add_line_to('define', line)

            # catch "modname" for use in pypi url rewriting
            if (line.startswith("%define") or line.startswith("%global")) and \
                 line.find("modname") >= 0:
                define, name, value = line.split(None, 2)
                self.modname = value

            return

        elif self.reg.re_prereq.match(line):
            match = self.reg.re_prereq.match(line)
            self._add_line_value_to('prereq', match.group(1))
            return

        elif self.reg.re_requires_phase.match(line):
            match = self.reg.re_requires_phase.match(line)
            # Put the requires content properly as key for formatting
            self._add_line_value_to('requires_phase', match.group(2), key='Requires{0}'.format(match.group(1)))
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
            # only store subpkgs if they have different licenses
            if not (type(self).__name__ == 'RpmPackage' and not self.subpkglicense):
                self._add_line_value_to('license', value)
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
            self._add_line_value_to('summary_localized', content, key='Summary{0}'.format(language))
            return

        elif self.reg.re_group.match(line):
            match = self.reg.re_group.match(line)
            value = match.group(1)
            if not self.minimal:
                if self.previous_line and not self.previous_line.startswith('# FIXME') and value not in self.allowed_groups:
                    self.paragraph.current_group.append('# FIXME: use correct group, see "https://en.opensuse.org/openSUSE:Package_group_guidelines"')
            self._add_line_value_to('group', value)
            return

        # loop for all other matching categories which
        # do not require special attention
        else:
            # cleanup
            for (category, regexp) in self.category_to_clean.items():
                match = regexp.match(line)
                if match:
                    return

            # simple matching
            for (category, regexp) in self.category_to_re.items():
                match = regexp.match(line)
                if match:
                    # instead of matching first group as there is only one,
                    # take the last group (including "whole match" if no groups present)
                    # (so I can have more advanced regexp for RPM tags)
                    self._add_line_value_to(category, match.group(len(match.groups())))
                    return

            self._add_line_to('misc', line)

    def output(self, fout, newline=True, new_class=None):
        lines = self.paragraph.flatten_output(self.subpkglicense)
        self.lines += lines
        Section.output(self, fout, newline, new_class)
