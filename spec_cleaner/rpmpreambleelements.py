# vim: set ts=4 sw=4 et: coding=UTF-8

from collections.abc import Iterable
from typing import Any, TypeAlias, cast

from .rpmexception import RpmExceptionError
from .rpmhelpers import (
    GroupItem,
    GroupLine,
    add_group,
    find_pkgconfig_declaration,
    find_pkgconfig_statement,
    fix_license,
    sort_uniq,
)
from .rpmregexp import Regexp
from .rpmrequirestoken import RpmRequiresToken

# a define unit: the lines of one %define/%global or a whole conditional
# block, as a list of the groups it consists of
Unit: TypeAlias = list[GroupItem]


class MacroLine(str):
    """
    Preamble line tagged with when rpm expands it.

    RpmPreamble.add sets the tags while parsing and the placement of the
    define units reads them. They survive the flattening of a nested
    block into its parent.
    """

    is_global = False
    is_cond = False
    is_eager = False

    def __new__(
        cls, line: str, is_global: bool = False, is_cond: bool = False, is_eager: bool = False
    ) -> 'MacroLine':
        """Create the tagged line."""
        tagged = super().__new__(cls, line)
        tagged.is_global = is_global
        tagged.is_cond = is_cond
        tagged.is_eager = is_eager
        return tagged


class _TrackedList(list[GroupItem]):
    """
    Bucket list reporting its elements to the owning RpmPreambleElements.

    The owner records the order in which elements were first added to
    any bucket; minimal mode uses that order to emit the preamble in
    source order instead of the canonical category order.

    Only the additions are instrumented: construction from an iterable,
    append, extend, += and insert report the elements they store —
    except a group rebuilt from recorded members, which construction
    leaves unrecorded so that it resolves through its earliest member.
    The list is append-only for ordering purposes — no other mutator
    (item assignment, pop, remove, sort, ...) reports anything, and no
    mutation updates a position once recorded. Mutating a stored group
    in place does not record the lines it gains, and the position the
    group resolves to does not change.
    """

    def __init__(self, owner: 'RpmPreambleElements', iterable: Iterable[GroupItem] = ()) -> None:
        """Create the list, reporting any initial elements to the owner."""
        super().__init__(iterable)
        self._owner = owner
        for element in self:
            # A group rebuilt from recorded members carries no position
            # of its own: the deduplication returns its buckets through
            # this wrapping, and a rebuilt group (merged comments of a
            # dropped duplicate) resolves through its earliest member
            # instead of the position of the rebuild.
            if isinstance(element, list) and owner._has_recorded_member(element):
                continue
            owner._record_position(element)

    def append(self, element: GroupItem) -> None:
        """Append the element, reporting it to the owner."""
        self._owner._record_position(element)
        super().append(element)

    def extend(self, elements: Iterable[GroupItem]) -> None:
        """Append all the elements, reporting them to the owner."""
        elements = list(elements)
        for element in elements:
            self._owner._record_position(element)
        super().extend(elements)

    # list.__add__/__iadd__ signature pairing cannot express the tracked
    # return, and insert narrows SupportsIndex to the int the callers pass
    def __iadd__(self, elements: Iterable[GroupItem]) -> '_TrackedList':  # type: ignore[misc, override]
        """Append all the elements, reporting them to the owner."""
        self.extend(elements)
        return self

    def insert(self, index: int, element: GroupItem) -> None:  # type: ignore[override]
        """Insert the element, reporting it to the owner."""
        self._owner._record_position(element)
        super().insert(index, element)


class _TrackedItems(dict[str, _TrackedList]):
    """Category dict wrapping every assigned bucket in a _TrackedList."""

    def __init__(self, owner: 'RpmPreambleElements') -> None:
        """Create the dict for the given RpmPreambleElements owner."""
        super().__init__()
        self._owner = owner

    def __setitem__(self, category: str, elements: _TrackedList | list[GroupItem]) -> None:
        """Store the bucket, wrapping plain lists so appends are reported."""
        if not isinstance(elements, _TrackedList):
            elements = _TrackedList(self._owner, elements)
        super().__setitem__(category, elements)


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
        'buildrequires_pragma': '#!BuildRequires',
        'buildconflicts': 'BuildConflicts',
        'buildconflicts_pragma': '#!BuildConflicts',
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
        'buildrequires_pragma',
        'buildconflicts',
        'buildconflicts_pragma',
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
        'buildroot',
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
        'buildrequires_pragma',
        'buildconflicts',
        'buildconflicts_pragma',
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

    def __init__(self, options: dict[str, Any]) -> None:
        """Initialize the default variables as some are dynamic."""
        self.items: _TrackedItems = _TrackedItems(self)
        for i in self.categories_order:
            self.items[i] = []
        # source position of every element added to a bucket, by identity;
        # minimal mode emits the buckets merged in this order
        self._positions: dict[int, int] = {}
        self._recorded: list[GroupItem] = []
        self._next_position = 0
        self.current_group: list[GroupItem] = []
        # minimal mode
        self.minimal: bool = options['minimal']
        # regexp object
        self.reg: Regexp = options['reg']
        # the main package's own -lang subpackage if the %lang_package macro generates it
        self.lang_package: set[str] = options.get('lang_package', set()) & {'%{name}-lang'}
        # pkgconfig requirement detection
        self.br_pkgconfig_required = False
        # license string
        self.license: str = options['license']
        # dict of license replacement options
        self.license_conversions: dict[str, str] = options['license_conversions']
        # initialize list of groups that need to pass over conversion fixer
        self.categories_with_package_tokens = self.categories_with_sorted_package_tokens[:]
        # these packages actually need fixing after we sent the values to
        # reorder them
        self.categories_with_package_tokens.append('provides_obsoletes')

    def _record_position(self, element: GroupItem) -> None:
        """
        Record the source position of an element added to a bucket.

        Only the first addition counts: an element the placement moves
        to another bucket keeps the position of where it was written.
        The members of a group are recorded with the group's position,
        so a group rebuilt from its members (merged comments, a
        conditional block split into units) still resolves to its
        source position. Only minimal mode reads the recording.
        """
        if not getattr(self, 'minimal', False) or id(element) in self._positions:
            return
        position = self._next_position
        self._next_position += 1
        stack = [element]
        while stack:
            item = stack.pop()
            if id(item) in self._positions:
                continue
            self._positions[id(item)] = position
            # keep a reference so the id cannot be recycled while the
            # paragraph is alive
            self._recorded.append(item)
            if isinstance(item, list):
                stack.extend(item)

    def _has_recorded_member(self, group: list[GroupItem]) -> bool:
        """Check whether any member of the group has a recorded position."""
        stack = list(group)
        while stack:
            item = stack.pop()
            if id(item) in self._positions:
                return True
            if isinstance(item, list):
                stack.extend(item)
        return False

    def _element_position(self, element: GroupItem) -> int | None:
        """
        Return the recorded source position of a bucket element.

        Elements rebuilt from recorded members (a conditional block
        split into define units, a group that absorbed the comments of
        a dropped duplicate) resolve through their earliest member.
        """
        position = self._positions.get(id(element))
        if position is not None or not isinstance(element, list):
            return position
        known = [
            member_position
            for item in element
            if (member_position := self._element_position(item)) is not None
        ]
        return min(known) if known else None

    def _sort_helper_key(self, a: GroupItem) -> int | str:
        key: int | str
        if isinstance(a, str) or isinstance(a, RpmRequiresToken):
            key = str(a)
        elif isinstance(a, list):
            # if this is a list then all items except last are comment or whitespace
            key = str(a[-1])
        else:
            raise RpmExceptionError(f'Unknown type during sort: {a}')

        # Special case is the category grouping where we have to get the number in
        # after the value
        match = self.reg.re_source.match(key)
        if match:
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

    def _sort_patches(self, patches: list[GroupItem]) -> list[GroupItem]:
        """Sort patches by number, an unnumbered Patch keeps the number rpm assigns it."""
        numbered: list[tuple[int, GroupItem]] = []
        last = -1
        for patch in patches:
            match = self.reg.re_patch.match(str(patch[-1] if isinstance(patch, list) else patch))
            # rpm numbers it after the highest patch number above it
            # (every line in the patch bucket matches re_patch by construction)
            number = int(match.group(2)) if match.group(2) else last + 1  # type: ignore[union-attr]
            last = max(last, number)
            numbered.append((number, patch))
        return [patch for _, patch in sorted(numbered, key=lambda pair: pair[0])]

    def _insert_value(self, category: str, value: str, key: str | None = None) -> None:
        """Add value to specified keystore."""
        key = self.compile_category_prefix(category, key)
        line = RpmRequiresToken(value, None, None, key)
        self.items[category].append(line)

    def _add_pkgconfig_buildrequires(self, nested: bool) -> None:
        """
        Check the content of buildrequires and add pkgconfig if needed.

        It adds pkgconfig as an item in case there are any pkgconfig() style
        dependencies present.

        If we are in the top level object for preamble we append the BR,
        otherwise we do just verify if there are nay dependencies
        """
        # first generate flat list from the BR
        buildrequires: list[GroupLine] = []
        for group in self.items['buildrequires']:
            buildrequires += add_group(group)
        # Check if we need the pkgconfig
        if not self.br_pkgconfig_required and find_pkgconfig_statement(buildrequires):
            self.br_pkgconfig_required = True
        # only in case we are in main scope
        if not nested:
            if self.br_pkgconfig_required and not find_pkgconfig_declaration(buildrequires):
                self._insert_value('buildrequires', 'pkgconfig')
                if self.minimal:
                    self._place_inserted_buildrequires()

    def _place_inserted_buildrequires(self) -> None:
        """
        Keep the inserted pkgconfig declaration with the BuildRequires lines.

        The declaration is created while flattening, so its recorded
        position is the newest one; in source order it belongs right
        after the last BuildRequires line it was derived from.
        """
        elements = self.items['buildrequires']
        known = [
            position
            for element in elements[:-1]
            if (position := self._element_position(element)) is not None
        ]
        if known:
            self._positions[id(elements[-1])] = max(known)

    @staticmethod
    def _verify_prereq_message(elements: list[GroupLine]) -> list[GroupLine]:
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
                # tokens in a paragraph always carry their category prefix
                if element.prefix.startswith('PreReq'):  # type: ignore[union-attr]
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
    def _plain_line(element: GroupItem) -> str | None:
        """
        Return the line an element holds if it is a plain string line.

        Plain lines are stored either directly or as the last item of a
        group whose preceding items are the comments belonging to the
        line; anything else returns None.
        """
        if isinstance(element, str):
            return element
        if isinstance(element, list) and element and isinstance(element[-1], str):
            return element[-1]
        return None

    @staticmethod
    def _absorb_line_comments(kept: GroupItem, dropped: GroupItem) -> GroupItem:
        """Return the kept element extended with the dropped one's comments."""
        comments: list[GroupItem] = []
        for element in (kept, dropped):
            if isinstance(element, list):
                comments += element[:-1]
        if not comments:
            return kept
        line = kept[-1] if isinstance(kept, list) else kept
        return comments + [line]

    @staticmethod
    def _remove_duplicates(elements: list[GroupItem]) -> list[GroupItem]:
        """Remove duplicate requires/buildrequires/etc."""
        results: list[GroupItem] = []
        for element in elements:
            match = False
            # anything else than requirestoken
            if not isinstance(element, RpmRequiresToken):
                # plain lines carry no token to compare (a suffixed #!
                # entry is kept whole as a string); an identical line
                # stored earlier makes this one a duplicate and the
                # comments merge the same way they do for tokens
                line = RpmPreambleElements._plain_line(element)
                if line is not None:
                    for index, item in enumerate(results):
                        if RpmPreambleElements._plain_line(item) == line:
                            results[index] = RpmPreambleElements._absorb_line_comments(
                                item, element
                            )
                            match = True
                            break
                if not match:
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
                        # (item is results[index]; the merge mutates it in place)
                        if element.comments:
                            if item.comments:
                                item.comments += element.comments
                            else:
                                item.comments = element.comments
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
                        # tokens in a paragraph always carry their category prefix
                        and not item.prefix.startswith(('Provides', 'Obsoletes'))  # type: ignore[union-attr]
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

    def _run_global_list_operations(self, phase: str, elements: list[GroupLine]) -> list[GroupLine]:
        """
        Run all the needed checks on the finalized sorted list.

        Run all the checks that need to be run on the finalized sorted list
        rather than on invidiual value.
        """
        # check if we need to add comment for the prereq
        if not self.minimal and phase == 'prereq':
            elements = self._verify_prereq_message(elements)

        return elements

    def compile_category_prefix(self, category: str, key: str | None = None) -> str:
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

        # key is always set here: passed in, taken from category_to_key,
        # or the unhandled category raised above
        assert key is not None
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

    def _is_own_lang_package(self, dep_name: str, package_name: str | None) -> bool:
        """Check if a dependency name references a -lang subpackage of %lang_package."""
        if self.reg.re_macro_spelling.sub(r'%{\1}', dep_name) in self.lang_package:
            return True
        # literal form, e.g. Recommends: foo-lang in foo.spec
        return (
            '%{name}-lang' in self.lang_package
            and bool(package_name)
            and dep_name == f'{package_name}-lang'
        )

    def _prune_lang_recommends(self) -> None:
        """
        Drop Recommends on the -lang subpackage when %lang_package is used.

        The macro generates Supplements for the lang subpackage, so a manual
        Recommends on it is redundant (#273). Without the macro (e.g. vlc)
        nothing else pulls the lang package in, so the line must stay.
        """
        if self.minimal or not self.lang_package:
            return
        package_name: str | None = None
        for group in self.items['name']:
            # the flattened name group ends in the Name line itself
            match = self.reg.re_name.match(add_group(group)[-1])  # type: ignore[arg-type]
            if match and match.group(1):
                package_name = match.group(1)
                break
        kept: list[GroupItem] = []
        for group in self.items['recommends']:
            redundant = False
            for item in add_group(group):
                dep_name: str | None = None
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

    def _macro_references(self, line: str) -> list[str]:
        """List the macros the line references, the with_ switch for %{with ...} included."""
        return self.reg.re_macro_reference.findall(line) + [
            'with_' + name for name in self.reg.re_bcond_reference.findall(line)
        ]

    def _bcond_switch(self, line: str) -> list[str]:
        """List the with_ switch the %bcond line defines."""
        match = self.reg.re_bcond_with.match(line)
        if match and match.group(3).split():
            return ['with_' + match.group(3).split()[0]]
        return []

    def _macro_definitions(self, line: str) -> list[str]:
        """List the macros the line defines, the with_ switch for a %bcond included."""
        return self.reg.re_macro_definition.findall(line) + self._bcond_switch(line)

    def _late_global_units(
        self, units: Iterable[GroupItem], bcond_macros: Iterable[str] = ()
    ) -> list[tuple[GroupItem, bool, bool]]:
        """
        Flag the define units to keep below the tags or the bconds.

        A unit is a single line, a multiline macro or a whole %if block, as
        RpmPreamble.add recorded it, so that moving it never breaks it apart.
        A unit is late when one of its globals or conditions references
        %name, %version, %release or %epoch, when one of its eagerly expanded
        lines references a late macro, or when it redefines one. A unit is
        also late when it invokes a section-generating macro (the tail
        macros, eg. %python_subpackages): the macro expands to %package
        sections built from the whole preamble, so the unit must stay
        below all of it, at the tail of the preamble. The macros a unit
        defines are late when it is late or references those tags or
        late macros, as a lazy %define that stays hoisted passes the
        dependency on to the globals using it.
        Likewise a unit must follow the bconds when one of its globals or
        conditions reads a bcond or a macro depending on one, or when it
        redefines a macro moved below the bconds.
        """
        late_names: set[str] = set()
        bcond_names: set[str] = set(bcond_macros)
        moved_names: set[str] = set()
        flagged: list[tuple[GroupItem, bool, bool]] = []
        for unit in units:
            lines = self._unit_lines(unit)
            definitions = [name for line in lines for name in self._macro_definitions(line)]
            # a redefinition must stay below the definition it overrides
            late = bool(late_names.intersection(definitions))
            after_bconds = bool(moved_names.intersection(definitions))
            tainted = bcond_tainted = False
            for line in lines:
                is_global = getattr(line, 'is_global', False)
                is_cond = getattr(line, 'is_cond', False)
                is_eager = getattr(line, 'is_eager', False)
                references = self._macro_references(line)
                sensitive = bool(self.reg.re_global_order_sensitive.search(line))
                reads_late = bool(late_names.intersection(references))
                if ((is_global or is_cond) and sensitive) or (is_eager and reads_late):
                    late = True
                if self.reg.re_tail_macros.match(line):
                    # the macro generates %package sections from the
                    # whole preamble, so the unit must close it
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
            flagged.append((unit, late, after_bconds))
        return flagged

    def _block_units(self, groups: list[GroupItem]) -> list[Unit]:
        """Split the lines of a closed conditional block into define units."""
        # a tail macro kept in the enclosing block precedes the opening line and moves alone
        lines = self._unit_lines(groups)
        conds = [i for i, line in enumerate(lines) if getattr(line, 'is_cond', False)]
        start = conds[0] if conds else len(groups)
        # a pruned block is empty, and an empty unit would still count as a define
        return [[group] for group in groups[:start]] + ([groups[start:]] if groups[start:] else [])

    def add_define_block(self, groups: list[GroupItem]) -> None:
        """Add a closed conditional block to the defines."""
        self.items['define'] += self._block_units(groups)

    def has_late_globals(self, block: list[GroupItem]) -> bool:
        """Check if the closed block must stay below the preamble tags."""
        return any(late for _, late, _ in self._late_global_units(self._block_units(block)))

    def reads_late_macros(self, block: list[GroupItem]) -> bool:
        """Check if the block after the defines reads a macro kept below the tags."""
        units = self.items['define'] + self._block_units(block)
        return bool(block) and self._late_global_units(units)[-1][1]

    def reads_moved_macros(self, block: list[GroupItem]) -> bool:
        """Check if the block after the defines reads a macro kept below the tags or bconds."""
        if not block:
            return False
        units = self.items['define'] + self._block_units(block)
        _, late, after_bconds = self._late_global_units(units, self._bcond_macros())[-1]
        return late or after_bconds

    def _bcond_macros(self) -> set[str]:
        """Collect the with_ switches of the bconds and the macros defined below them."""
        names: set[str] = set()
        for category in ('define', 'bconds', 'bcond_conditions'):
            for group in self.items[category]:
                for line in add_group(group):
                    # the define/bcond buckets hold plain lines, never tokens
                    text = cast(str, line)
                    names.update(self._bcond_switch(text))
                    # the define blocks placed with the bconds precede all the other defines
                    if category != 'define':
                        names.update(self.reg.re_macro_definition.findall(text))
        return names

    def _split_late_globals(self, nested: bool) -> None:
        """
        Move the define units below the Version/Release tags or the bconds when needed.

        %global expands its value immediately, so a global referencing macros
        that rpm defines while parsing the preamble tags (%name, %version,
        %release, %epoch) breaks when hoisted above those tags (#239), and one
        reading a bcond breaks when hoisted above the %bcond lines. Such a
        global moves with its whole unit (see _late_global_units), any %define
        in it included. A unit invoking a section-generating macro (eg.
        %python_subpackages) moves to the tail of the preamble instead, as
        the macro builds its %package sections from the whole preamble.
        Everything else stays hoisted at the top, and so do the units
        defining macros the tags use, with the units those depend on.
        Nested %if blocks move whole, so only a level holding the tags or the
        bconds splits.
        """
        flagged = self._late_global_units(self.items['define'], self._bcond_macros())
        self._keep_tag_dependencies(flagged, self._tag_references())
        self._place_define_units(flagged, nested)

    @staticmethod
    def _unit_lines(unit: GroupItem) -> list[str]:
        """List the lines of the unit, leaving out the comments grouped with them."""
        # a unit is a list of groups by construction, and each group ends
        # in the line itself (a string), the comments grouped with it aside
        return [cast(str, add_group(group)[-1]) for group in cast(Unit, unit)]

    def _tag_references(self) -> set[str]:
        """Collect the macros the preamble tags and the conditions holding them read."""
        return {
            name
            for category in ('head', 'name', 'version', 'release', 'epoch', 'nvr_conditions')
            for group in self.items[category]
            for line in add_group(group)
            for name in self._macro_references(str(line))
        }

    def _keep_tag_dependencies(
        self, flagged: list[tuple[GroupItem, bool, bool]], needed: set[str]
    ) -> None:
        """Keep the units defining macros the tags read on top, with the units they read."""
        # dependencies precede their users, so one backward pass collects them all
        for index in reversed(range(len(flagged))):
            unit, _, after_bconds = flagged[index]
            lines = self._unit_lines(unit)
            definitions = [name for line in lines for name in self._macro_definitions(line)]
            if needed.intersection(definitions):
                flagged[index] = (unit, False, after_bconds)
                needed.update(name for line in lines for name in self._macro_references(line))

    def _invokes_tail_macro(self, unit: GroupItem) -> bool:
        """Check if the unit invokes a section-generating macro (the tail macros)."""
        return any(self.reg.re_tail_macros.match(line) for line in self._unit_lines(unit))

    def _place_define_units(
        self, flagged: list[tuple[GroupItem, bool, bool]], nested: bool
    ) -> None:
        """Place each flagged unit on top, below the tags or below the bconds."""
        has_tags = any(
            self.items[i] for i in ('name', 'version', 'release', 'epoch', 'nvr_conditions')
        )
        has_bconds = any(self.items[i] for i in ('bconds', 'bcond_conditions'))
        self.items['define'] = []
        for unit, late, after_bconds in flagged:
            # a unit is a list of groups by construction; the += sites
            # below extend a bucket with the unit's groups
            groups = cast(Unit, unit)
            if not nested and self._invokes_tail_macro(unit):
                # the macro generates %package sections from the whole
                # preamble, so the unit closes the preamble at the tail;
                # in a nested paragraph the unit stays with the defines
                # and the enclosing level routes the whole block instead
                self.items['tail'] += groups
            elif late and (has_tags or not nested):
                self.items['global_late'] += groups
            elif after_bconds and (has_bconds or not nested):
                self.items['bcond_conditions'] += groups
            else:
                self.items['define'].append(unit)

    def _flatten_in_source_order(self) -> list[str]:
        """
        Emit the buckets merged by source position (minimal mode).

        Every element recorded the position at which it was first added
        to a bucket, so merging by that position restores the order the
        lines had in the source file: conditional blocks stay where
        they were written, in the order they were written, and no line
        crosses the Name: tag. The transformations that only edit lines
        in place (the deduplication above, the inserted pkgconfig
        declaration) still apply; sorting and define relocation do not.
        """
        gathered: list[tuple[str, GroupItem]] = []
        for category in self.categories_order:
            gathered += [(category, group) for group in self.items[category]]
        positioned: list[tuple[int | None, str, GroupItem]] = []
        last: int | None = None
        for category, group in gathered:
            position = self._element_position(group)
            if position is None:
                # an element rebuilt from unrecorded parts inherits the
                # position of the element gathered before it
                position = last
            else:
                last = position
            positioned.append((position, category, group))
        # the sort is stable: elements sharing a position (the inserted
        # pkgconfig declaration shares its anchor's) keep gathering order;
        # an element whose position is still None stood at the head,
        # before every recorded element, so it sorts first
        positioned.sort(key=lambda item: -1 if item[0] is None else item[0])
        seen: set[tuple[str, ...]] = set()
        lines: list[GroupLine] = []
        for _, category, group in positioned:
            group_lines = add_group(group)
            if category in self.categories_with_sorted_keyword_tokens:
                # the canonical order sorts these categories and drops
                # duplicates; source order keeps the lines as written
                # but still drops exact duplicates
                text = tuple(str(line) for line in group_lines)
                if text in seen:
                    continue
                seen.add(text)
            lines += self._run_global_list_operations(category, group_lines)
        if self.current_group:
            # the current group was not added to any category. It's just some
            # random stuff that should be at the end anyway.
            lines += add_group(self.current_group)
            self.current_group = []
        return [line if isinstance(line, str) else str(line) for line in lines]

    def flatten_output(self, needs_license: bool = False, nested: bool = False) -> list[str]:
        """Do the finalized output for the itemlist."""
        lines: list[GroupLine] = []
        elements: list[str] = []

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
        if self.minimal:
            # minimal mode does not reorder: the buckets are emitted in
            # source order and no define unit is relocated
            return self._flatten_in_source_order()
        # keep version-dependent globals below the tags (#239) and bcond readers below the bconds
        self._split_late_globals(nested)
        for i in self.categories_order:
            sorted_list: list[GroupLine] = []
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
            # a MacroLine keeps its tags for the define units of the parent block
            elements.append(line if isinstance(line, str) else str(line))
        return elements
