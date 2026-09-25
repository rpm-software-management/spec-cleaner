# vim: set ts=4 sw=4 et: coding=UTF-8

from .rpmexception import RpmExceptionError
from .rpmhelpers import (
    add_group,
    find_pkgconfig_declaration,
    find_pkgconfig_statement,
    fix_license,
    sort_uniq,
)
from .rpmrequirestoken import RpmRequiresToken


class RpmPreambleElements:
    """
    Class containing structure used in rpmpreamble.

    List of all the elements possible to be provided in dict and list forms.
    """

    category_to_key = {
        'name': 'Name',
        'version': 'Version',
        'release': 'Release',
        'epoch': 'Epoch',
        'license': 'License',
        'summary': 'Summary',
        # The localized summary can contain various values, so it can't be here
        'url': 'URL',
        'group': 'Group',
        'source': 'Source',
        'nosource': 'NoSource',
        'patch': 'Patch',
        'buildsystem': 'BuildSystem',
        'buildoption': 'BuildOption',
        'buildrequires': 'BuildRequires',
        'buildconflicts': 'BuildConflicts',
        'buildignores': '#!BuildIgnore',
        'conflicts': 'Conflicts',
        'prereq': 'PreReq',
        'requires': 'Requires',
        'requires_eq': '%requires_eq',
        'requires_ge': '%requires_ge',
        'recommends': 'Recommends',
        'suggests': 'Suggests',
        'enhances': 'Enhances',
        'supplements': 'Supplements',
        # Provides/Obsoletes cannot be part of this since we want to keep them
        # mixed, so we'll have to specify the key when needed
        'buildarch': 'BuildArch',
        'exclusivearch': 'ExclusiveArch',
        'excludearch': 'ExcludeArch',
        'removepath': 'RemovePathPostfixes',
    }

    categories_order = (
        'define',
        'bconds',
        'bcond_conditions',
        'head',
        'name',
        'version',
        'release',
        'epoch',
        'nvr_conditions',
        # %global lines that reference macros defined by the preamble tags
        # above; they cannot be hoisted to the top as %global expands
        # immediately (#239)
        'global_late',
        'summary',
        'summary_localized',
        'license',
        'group',
        'url',
        'source',
        'nosource',
        'patch',
        'buildsystem',
        'buildoption',
        'buildoption_phase',
        'patternprovides',  # fake provides with special function for patterns
        'patternrequires',  # fake requires with special function for patterns
        'patternrecommends',  # fake recommends with special function for patterns
        'patternsuggests',  # fake suggests with special function for patterns
        'patternobsoletes',  # fake provide/obsoletes with old pattern symbols
        'patterncodeblock',  # fake condition placement for patterns to stay on top
        'buildrequires',
        'buildconflicts',
        'buildignores',
        'requires',
        'requires_eq',
        'requires_ge',
        'prereq',
        'requires_phase',  # this is Requires(pre/post/...)
        'recommends',
        'suggests',
        'enhances',
        'supplements',
        'conflicts',
        'provides_obsoletes',
        'removepath',
        'buildarch',
        'exclusivearch',
        'excludearch',
        'misc',
        'build_conditions',
        'conditions',
        'tail',
        # a block whose %endif follows the next section header
        'open_conditions',
    )

    # categories that are sorted based on value in them
    categories_with_sorted_package_tokens = [
        'patternprovides',
        'patternrequires',
        'patternrecommends',
        'patternsuggests',
        'buildrequires',
        'buildconflicts',
        'buildignores',
        'prereq',
        'requires',
        'requires_eq',
        'requires_ge',
        'requires_phase',
        'recommends',
        'suggests',
        'enhances',
        'supplements',
        'conflicts',
    ]

    # categories that are sorted based on key value (eg Patch0 before Patch1)
    categories_with_sorted_keyword_tokens = ('source', 'patch')

    def __init__(self, options):
        """Initialize the default variables as some are dynamic."""
        self.items = {}
        for i in self.categories_order:
            self.items[i] = []
        self.current_group = []
        # minimal mode
        self.minimal = options['minimal']
        # regexp object
        self.reg = options['reg']
        # the main package's own -lang subpackage if the %lang_package macro generates it
        self.lang_package = options.get('lang_package', set()) & {'%{name}-lang'}
        # pkgconfig requirement detection
        self.br_pkgconfig_required = False
        # license string
        self.license = options['license']
        # dict of license replacement options
        self.license_conversions = options['license_conversions']
        # initialize list of groups that need to pass over conversion fixer
        self.categories_with_package_tokens = self.categories_with_sorted_package_tokens[:]
        # these packages actually need fixing after we sent the values to
        # reorder them
        self.categories_with_package_tokens.append('provides_obsoletes')

    def _sort_helper_key(self, a):
        if isinstance(a, str) or isinstance(a, RpmRequiresToken):
            key = str(a)
        elif isinstance(a, list):
            # if this is a list then all items except last are comment or whitespace
            key = str(a[-1])
        else:
            raise RpmExceptionError(f'Unknown type during sort: {a}')

        # Special case is the category grouping where we have to get the number in
        # after the value
        if self.reg.re_source.match(key):
            match = self.reg.re_source.match(key)
            value = match.group(1)
            if not value:
                value = '1'
            key = int(value)
        # Put brackety ()-style deps at the end of the list, after all other
        elif self.reg.re_brackety_requires.search(key):
            key = '2' + key
        elif self.reg.re_patternmacro.search(key):
            key = '0' + key
        else:
            key = '1' + key
        return key

    def _sort_patches(self, patches):
        """Sort patches by number, an unnumbered Patch keeps the number rpm assigns it."""
        numbered = []
        last = -1
        for patch in patches:
            match = self.reg.re_patch.match(str(patch[-1] if isinstance(patch, list) else patch))
            # rpm numbers it after the highest patch number above it
            number = int(match.group(2)) if match.group(2) else last + 1
            last = max(last, number)
            numbered.append((number, patch))
        return [patch for _, patch in sorted(numbered, key=lambda pair: pair[0])]

    def _insert_value(self, category, value, key=None):
        """Add value to specified keystore."""
        key = self.compile_category_prefix(category, key)
        line = RpmRequiresToken(value, None, None, key)
        self.items[category].append(line)

    def _add_pkgconfig_buildrequires(self, nested):
        """
        Check the content of buildrequires and add pkgconfig if needed.

        It adds pkgconfig as an item in case there are any pkgconfig() style
        dependencies present.

        If we are in the top level object for preamble we append the BR,
        otherwise we do just verify if there are nay dependencies
        """
        # first generate flat list from the BR
        buildrequires = []
        for group in self.items['buildrequires']:
            buildrequires += add_group(group)
        # Check if we need the pkgconfig
        if not self.br_pkgconfig_required and find_pkgconfig_statement(buildrequires):
            self.br_pkgconfig_required = True
        # only in case we are in main scope
        if not nested:
            if self.br_pkgconfig_required and not find_pkgconfig_declaration(buildrequires):
                self._insert_value('buildrequires', 'pkgconfig')

    @staticmethod
    def _verify_prereq_message(elements):
        """
        Verify if prereq is present in Requires(*).

        Add "fixme" comment if needed.
        """
        message = '# FIXME: use proper Requires(pre/post/preun/...)'

        prereq_found = False
        message_found = False

        # Check first if we have prereq values included
        for element in elements:
            if isinstance(element, RpmRequiresToken):
                if element.prefix.startswith('PreReq'):
                    prereq_found = True
                    break
        if not prereq_found:
            return elements

        # Verify the message is not already present
        for element in elements:
            if isinstance(element, str):
                if element.startswith(message):
                    message_found = True
        if message_found:
            return elements

        # add the message on the first position after any whitespace
        location = next(i for i, j in enumerate(elements) if j)
        elements.insert(location, message)

        return elements

    @staticmethod
    def _remove_duplicates(elements):
        """Remove duplicate requires/buildrequires/etc."""
        results = []
        for element in elements:
            match = False
            # anything else than requirestoken
            if not isinstance(element, RpmRequiresToken):
                results.append(element)
                continue
            # no results stored yet
            if not results:
                results.append(element)
                continue
            # search already stored content
            for index, item in enumerate(results):
                # if item is string we didn't match
                if not isinstance(item, RpmRequiresToken):
                    continue
                # names and prefix must always match
                if item.name == element.name and item.prefix == element.prefix:
                    # do we have full match on everything
                    if item.version == element.version and item.operator == element.operator:
                        # append comment if needed only as we are 100% match
                        if element.comments:
                            tmp = results[index]
                            if tmp.comments:
                                tmp.comments += element.comments
                            else:
                                tmp.comments = element.comments
                            results[index] = tmp
                        match = True
                        break
                    # new one specifies version
                    if not item.version and element.version:
                        if item.comments:
                            if element.comments:
                                element.comments += item.comments
                            else:
                                element.comments = item.comments
                        results[index] = element
                        match = True
                        break
                    # existing one specifies version, the new one is subsumed
                    # by it no matter in which order they were written
                    # (not for Provides/Obsoletes, where unversioned means every version)
                    if (
                        item.version
                        and not element.version
                        and not item.prefix.startswith(('Provides', 'Obsoletes'))
                    ):
                        if element.comments:
                            item.comments = (item.comments or []) + element.comments
                        match = True
                        break
                    # for version determination which could be ommited one
                    # must use rpm versionCompare to get same results
                    # unfortunately it uses too many resources so we simply
                    # leave this to the maintainer
            if not match:
                results.append(element)
        return results

    def _run_global_list_operations(self, phase, elements):
        """
        Run all the needed checks on the finalized sorted list.

        Run all the checks that need to be run on the finalized sorted list
        rather than on invidiual value.
        """
        # check if we need to add comment for the prereq
        if not self.minimal and phase == 'prereq':
            elements = self._verify_prereq_message(elements)

        return elements

    def compile_category_prefix(self, category, key=None):
        """
        Provide enough whitespace so the values are aligned.

        Simply compile the category key and provide enough whitespace for the values
        to be aligned.
        """
        keylen = len('BuildRequires:  ')

        if category == 'tail':
            return ''
        if category == 'head':
            return ''
        elif key:
            pass
        elif category in self.category_to_key:
            key = self.category_to_key[category]
        else:
            raise RpmExceptionError(f'Unhandled category in preamble: {category}')

        # append : only if the thing is not known macro
        if not key.startswith('%'):
            key += ':'
        # if the key is already longer then just add one space
        if len(key) >= keylen:
            key += ' '
        # fillup rest of the alignment if key is shorter than muster
        while len(key) < keylen:
            key += ' '
        return key

    def _is_own_lang_package(self, dep_name, package_name):
        """Check if a dependency name references a -lang subpackage of %lang_package."""
        if self.reg.re_macro_spelling.sub(r'%{\1}', dep_name) in self.lang_package:
            return True
        # literal form, e.g. Recommends: foo-lang in foo.spec
        return (
            '%{name}-lang' in self.lang_package
            and bool(package_name)
            and dep_name == f'{package_name}-lang'
        )

    def _prune_lang_recommends(self):
        """
        Drop Recommends on the -lang subpackage when %lang_package is used.

        The macro generates Supplements for the lang subpackage, so a manual
        Recommends on it is redundant (#273). Without the macro (e.g. vlc)
        nothing else pulls the lang package in, so the line must stay.
        """
        if self.minimal or not self.lang_package:
            return
        package_name = None
        for group in self.items['name']:
            match = self.reg.re_name.match(add_group(group)[-1])
            if match and match.group(1):
                package_name = match.group(1)
                break
        kept = []
        for group in self.items['recommends']:
            redundant = False
            for item in add_group(group):
                dep_name = None
                if isinstance(item, RpmRequiresToken):
                    dep_name = item.name
                elif isinstance(item, str) and not item.startswith('#'):
                    match = self.reg.re_recommends.match(item)
                    if match and match.group(1).split():
                        dep_name = match.group(1).split()[0]
                if dep_name and self._is_own_lang_package(dep_name, package_name):
                    redundant = True
                    break
            if not redundant:
                kept.append(group)
        self.items['recommends'] = kept

    def _macro_references(self, line):
        """List the macros the line references, the with_ switch for %{with ...} included."""
        return self.reg.re_macro_reference.findall(line) + [
            'with_' + name for name in self.reg.re_bcond_reference.findall(line)
        ]

    def _bcond_switch(self, line):
        """List the with_ switch the %bcond line defines."""
        match = self.reg.re_bcond_with.match(line)
        if match and match.group(3).split():
            return ['with_' + match.group(3).split()[0]]
        return []

    def _macro_definitions(self, line):
        """List the macros the line defines, the with_ switch for a %bcond included."""
        return self.reg.re_macro_definition.findall(line) + self._bcond_switch(line)

    def _late_global_units(self, groups, bcond_macros=()):
        """
        Group the define lines into units, flagging the ones to keep below the tags.

        A unit is a single line, a multiline macro or a whole %if block, so
        that moving it never breaks it apart. A unit is late when one of its
        globals references %name, %version, %release or %epoch, when one of
        its globals or conditions references a late macro, or when it
        redefines one. The macros a unit defines are late when it is late or
        references those tags or late macros, as a lazy %define that stays
        hoisted passes the dependency on to the globals using it.
        Likewise a unit must follow the bconds when one of its globals or
        conditions reads a bcond or a macro depending on one, or when it
        redefines a macro moved below the bconds.
        """
        units = []
        depth = 0
        cond_braces = 0
        continuing = expand = run_global = cond_continuing = False
        expand_depth = 0
        for group in groups:
            line = add_group(group)[-1]
            if not (depth or continuing):
                units.append([])
            is_global = is_cond = is_eager = False
            # follows the multiline and condition parsing of RpmPreamble.add
            if cond_continuing:
                is_cond = is_eager = True
            elif continuing:
                is_global = is_eager = run_global
                if expand:
                    expand_depth += line.count('{') - line.count('}')
                    continuing = expand_depth > 0
                else:
                    continuing = line.endswith('\\')
            elif self.reg.re_if.match(line) or self.reg.re_codeblock.match(line):
                depth += 1
                is_cond = is_eager = True
            elif self.reg.re_multilinecond.match(line):
                depth += 1
                cond_braces += 1
                is_cond = is_eager = True
            elif depth and (self.reg.re_endif.match(line) or self.reg.re_endcodeblock.match(line)):
                depth -= 1
            elif cond_braces and self.reg.re_endmultilinecond.match(line):
                depth -= 1
                cond_braces -= 1
            elif self.reg.re_else_elif.match(line):
                is_cond = is_eager = True
            elif (
                self.reg.re_define.match(line)
                or self.reg.re_global.match(line)
                or self.reg.re_onelinecond.match(line)
            ):
                is_global = bool(self.reg.re_global.match(line)) or (
                    bool(self.reg.re_onelinecond.match(line)) and '%global' in line
                )
                run_global = is_global
                # a one-line condition is evaluated when parsed, even around %define
                is_eager = is_global or bool(self.reg.re_onelinecond.match(line))
                expand_depth = line.count('{') - line.count('}')
                expand = '%{expand:' in line and expand_depth > 0
                continuing = line.endswith('\\') or expand
            cond_continuing = is_cond and line.endswith('\\')
            units[-1].append((group, line, is_global, is_cond, is_eager))

        late_names = set()
        bcond_names = set(bcond_macros)
        moved_names = set()
        flagged = []
        for unit in units:
            definitions = [
                name for _, line, _, _, _ in unit for name in self._macro_definitions(line)
            ]
            # a redefinition must stay below the definition it overrides
            late = bool(late_names.intersection(definitions))
            after_bconds = bool(moved_names.intersection(definitions))
            tainted = bcond_tainted = False
            for _, line, is_global, is_cond, is_eager in unit:
                references = self._macro_references(line)
                sensitive = bool(self.reg.re_global_order_sensitive.search(line))
                reads_late = bool(late_names.intersection(references))
                if (is_global and sensitive) or ((is_global or is_cond) and reads_late):
                    late = True
                if sensitive or reads_late:
                    tainted = True
                if '%{with' in line or bcond_names.intersection(references):
                    bcond_tainted = True
                    if is_eager:
                        after_bconds = True
            if tainted or late:
                late_names.update(definitions)
            if bcond_tainted or after_bconds:
                bcond_names.update(definitions)
            if after_bconds:
                moved_names.update(definitions)
            flagged.append(([group for group, _, _, _, _ in unit], late, after_bconds))
        return flagged

    def has_late_globals(self, groups):
        """Check if any of the define groups must stay below the preamble tags."""
        return any(late for _, late, _ in self._late_global_units(groups))

    def reads_late_macros(self, block):
        """Check if the block after the defines reads a macro kept below the tags."""
        return bool(block) and self._late_global_units(self.items['define'] + block)[-1][1]

    def reads_moved_macros(self, block):
        """Check if the block after the defines reads a macro kept below the tags or bconds."""
        _, late, after_bconds = self._late_global_units(
            self.items['define'] + block, self._bcond_macros()
        )[-1]
        return late or after_bconds

    def _bcond_macros(self):
        """Collect the with_ switches of the bconds and the macros defined below them."""
        names = set()
        for category in ('define', 'bconds', 'bcond_conditions'):
            for group in self.items[category]:
                for line in add_group(group):
                    names.update(self._bcond_switch(line))
                    # the define blocks placed with the bconds precede all the other defines
                    if category != 'define':
                        names.update(self.reg.re_macro_definition.findall(line))
        return names

    def _split_late_globals(self, nested):
        """
        Move the define units below the Version/Release tags or the bconds when needed.

        %global expands its value immediately, so a global referencing macros
        that rpm defines while parsing the preamble tags (%name, %version,
        %release, %epoch) breaks when hoisted above those tags (#239), and one
        reading a bcond breaks when hoisted above the %bcond lines. Such a
        global moves with its whole unit (see _late_global_units), any %define
        in it included. Everything else stays hoisted at the top, and so do
        the units defining macros the tags use, with the units those depend on.
        Nested %if blocks move whole, so only a level holding the tags or the
        bconds splits.
        """
        flagged = self._late_global_units(self.items['define'], self._bcond_macros())
        needed = {
            name
            for category in ('head', 'name', 'version', 'release', 'epoch', 'nvr_conditions')
            for group in self.items[category]
            for line in add_group(group)
            for name in self._macro_references(str(line))
        }
        # dependencies precede their users, so one backward pass collects them all
        for index in reversed(range(len(flagged))):
            unit, _, after_bconds = flagged[index]
            lines = [add_group(group)[-1] for group in unit]
            definitions = [name for line in lines for name in self._macro_definitions(line)]
            if needed.intersection(definitions):
                flagged[index] = (unit, False, after_bconds)
                needed.update(name for line in lines for name in self._macro_references(line))
        has_tags = any(
            self.items[i] for i in ('name', 'version', 'release', 'epoch', 'nvr_conditions')
        )
        has_bconds = any(self.items[i] for i in ('bconds', 'bcond_conditions'))
        self.items['define'] = []
        for unit, late, after_bconds in flagged:
            if late and (has_tags or not nested):
                self.items['global_late'] += unit
            elif after_bconds and (has_bconds or not nested):
                self.items['bcond_conditions'] += unit
            else:
                self.items['define'] += unit

    def flatten_output(self, needs_license=False, nested=False):
        """Do the finalized output for the itemlist."""
        lines = []
        elements = []

        # add license to the package if missing and needed
        if needs_license and self.license and not self.items['license']:
            self.license = fix_license(self.license, self.license_conversions)
            self._insert_value('license', self.license)
        # add pkgconfig dep
        self._add_pkgconfig_buildrequires(nested)
        # remove duplicates
        for i in self.categories_with_package_tokens:
            self.items[i] = self._remove_duplicates(self.items[i])
        # drop Recommends on the -lang subpackage, the %lang_package macro
        # already generates Supplements for it (#273)
        self._prune_lang_recommends()
        # keep version-dependent globals below the tags (#239) and bcond readers below the bconds
        self._split_late_globals(nested)
        for i in self.categories_order:
            sorted_list = []
            if i in self.categories_with_sorted_package_tokens:
                self.items[i].sort(key=self._sort_helper_key)
            # sort-out within the ordered groups based on the key
            if i in self.categories_with_sorted_keyword_tokens:
                if i == 'patch':
                    self.items[i] = self._sort_patches(self.items[i])
                else:
                    self.items[i].sort(key=self._sort_helper_key)
                self.items[i] = sort_uniq(self.items[i])
            # flatten the list from list of lists as no reordering is planned
            for group in self.items[i]:
                sorted_list += add_group(group)
            # now do all sorts of operations where we needed sorted lists
            lines += self._run_global_list_operations(i, sorted_list)
        if self.current_group:
            # the current group was not added to any category. It's just some
            # random stuff that should be at the end anyway.
            lines += add_group(self.current_group)
            self.current_group = []

        for line in lines:
            elements.append(str(line))
        return elements
