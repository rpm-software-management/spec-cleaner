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


class RpmPreambleElements(object):
    """
    Class containing structure used in rpmpreamble.

    List of all the elements possible to be provided in dict and list forms.
    """

    category_to_key = {
        'name': 'Name',
        'version': 'Version',
        'release': 'Release',
        'license': 'License',
        'summary': 'Summary',
        # The localized summary can contain various values, so it can't be here
        'url': 'URL',
        'group': 'Group',
        'source': 'Source',
        'nosource': 'NoSource',
        'patch': 'Patch',
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
        'summary',
        'summary_localized',
        'license',
        'group',
        'url',
        'source',
        'nosource',
        'patch',
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
            raise RpmExceptionError('Unknown type during sort: %s' % a)

        # Special case is the category grouping where we have to get the number in
        # after the value
        if self.reg.re_patch.match(key):
            match = self.reg.re_patch.match(key)
            key = int(match.group(2))
        elif self.reg.re_source.match(key):
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
            raise RpmExceptionError('Unhandled category in preamble: %s' % category)

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

    def flatten_output(self, needs_license=False, nested=False):
        """Do the finalized output for the itemlist."""
        lines = []
        elements = []

        # add license to the package if missing and needed
        if needs_license and not self.items['license']:
            self.license = fix_license(self.license, self.license_conversions)
            self._insert_value('license', self.license)
        # add pkgconfig dep
        self._add_pkgconfig_buildrequires(nested)
        # remove duplicates
        for i in self.categories_with_package_tokens:
            self.items[i] = self._remove_duplicates(self.items[i])
        for i in self.categories_order:
            sorted_list = []
            if i in self.categories_with_sorted_package_tokens:
                self.items[i].sort(key=self._sort_helper_key)
            # sort-out within the ordered groups based on the key
            if i in self.categories_with_sorted_keyword_tokens:
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
