# vim: set ts=4 sw=4 et: coding=UTF-8

from .rpmhelpers import sort_uniq, add_group, find_pkgconfig_statement, find_pkgconfig_declaration, fix_license
from .rpmexception import RpmException

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
        'url': 'Url',
        'group': 'Group',
        'source': 'Source',
        'nosource': 'NoSource',
        'patch': 'Patch',
        'buildrequires': 'BuildRequires',
        'conflicts': 'Conflicts',
        'prereq': 'PreReq',
        'requires': 'Requires',
        'requires_eq': '%requires_eq',
        'recommends': 'Recommends',
        'suggests': 'Suggests',
        'enhances': 'Enhances',
        'supplements': 'Supplements',
        # Provides/Obsoletes cannot be part of this since we want to keep them
        # mixed, so we'll have to specify the key when needed
        'buildroot': 'BuildRoot',
        'buildarch': 'BuildArch',
        'exclusivearch': 'ExclusiveArch',
        'excludearch': 'ExcludeArch',
    }

    categories_order = [
        'define',
        'bconds',
        'bcond_conditions',
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
        'buildrequires',
        'requires',
        'requires_eq',
        'prereq',
        'requires_phase',  # this is Requires(pre/post/...)
        'recommends',
        'suggests',
        'enhances',
        'supplements',
        'conflicts',
        'provides_obsoletes',
        'buildroot',
        'buildarch',
        'exclusivearch',
        'excludearch',
        'misc',
        'build_conditions',
        'conditions',
    ]

    # categories that are sorted based on value in them
    categories_with_sorted_package_tokens = [
        'buildrequires',
        'prereq',
        'requires',
        'requires_eq',
        'requires_phase',
        'recommends',
        'suggests',
        'enhances',
        'supplements',
        'conflicts',
    ]

    # categories that are sorted based on key value (eg Patch0 before Patch1)
    categories_with_sorted_keyword_tokens = [
        'source',
        'patch',
    ]

    def __init__(self, options):
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

    def _sort_helper_key(self, a):
        t = type(a)
        if t == str:
            key = a
        elif t == list:
            # if this is a list then all items except last are comment or whitespace
            key = a[-1]
        else:
            raise RpmException('Unknown type during sort: %s' % t)

        # Special case is the category grouping where we have to get the number in
        # after the value
        if self.reg.re_patch.match(key):
            match = self.reg.re_patch.match(key)
            key = int(match.group(2))
        elif self.reg.re_source.match(key):
            match = self.reg.re_source.match(key)
            value = match.group(1)
            if not value:
                value = '0'
            key = int(value)
        # Put brackety ()-style deps at the end of the list, after all other
        elif self.reg.re_brackety_requires.search(key):
            key = '1' + key
        else:
            key = '0' + key
        return key
    
    def _insert_value(self, category, value, key = None):
        """
        Add value to specified keystore
        """
        key = self.compile_category_prefix(category, key)
        line = key + value
        self.items[category].append(line)

    def _add_pkgconfig_buildrequires(self, nested):
        """
        Check the content of buildrequires and add pkgconfig as an item
        in case there are any pkgconfig() style dependencies present
        
        If we are in the top level object for preamble we append the BR,
        otherwise we do just verify if there are nay dependencies
        """
        # first generate flat list from the BR
        buildrequires = []
        for group in self.items['buildrequires']:
            buildrequires += add_group(group)
        # Check if we need the pkgconfig
        if not self.br_pkgconfig_required and \
           find_pkgconfig_statement(buildrequires):
            self.br_pkgconfig_required = True
        # only in case we are in main scope
        if not nested:
            if self.br_pkgconfig_required and not find_pkgconfig_declaration(buildrequires):
                self._insert_value('buildrequires', 'pkgconfig')

    def _verify_prereq_message(self, elements):
        """
        Verify if the prereq is present in the Requires(*) and add the fixme
        comment if needed
        """
        message = '# FIXME: use proper Requires(pre/post/preun/...)'

        # Check first if we have prereq values included
        if not any("PreReq" in s for s in elements):
            return elements

        # Verify the message is not already present
        if any(message in s for s in elements):
            return elements

        # add the message on the first position after any whitespace
        location = next(i for i, j in enumerate(elements) if j)
        elements.insert(location, message)

        return elements

    def _run_global_list_operations(self, phase, elements):
        """
        Run all the checks that need to be run on the finalized sorted list
        rather than on invidiual value
        """
        # check if we need to add comment for the prereq
        if not self.minimal and phase == 'prereq':
            elements = self._verify_prereq_message(elements)

        return elements

    def compile_category_prefix(self, category, key=None):
        """
        Simply compile the category key and provide enough whitespace for the
        values to be alligned
        """
        keylen = len('BuildRequires:  ')

        if key:
            pass
        elif category in self.category_to_key:
            key = self.category_to_key[category]
        else:
            raise RpmException('Unhandled category in preamble: %s' % category)

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

    def flatten_output(self, needs_license=False, nested = False):
        """
        Do the finalized output for the itemlist.
        """
        lines = []

        # add license to the package if missing and needed
        if needs_license and not self.items['license']:
            self.license = fix_license(self.license, self.license_conversions)
            self._insert_value('license', self.license)
        # add pkgconfig dep
        self._add_pkgconfig_buildrequires(nested)
        for i in self.categories_order:
            sorted_list = []
            # sort-out within the ordered groups based on the key
            if i in self.categories_with_sorted_package_tokens + self.categories_with_sorted_keyword_tokens:
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
        return lines
