# vim: set ts=4 sw=4 et: coding=UTF-8

import re

from rpmsection import Section
from fileutils import FileUtils


LICENSES_CHANGES = 'licenses_changes.txt'
PKGCONFIG_CONVERSIONS = 'pkgconfig_conversions.txt'


class RpmPreamble(Section):
    """
        Only keep one empty line for many consecutive ones.
        Reorder lines.
        Fix bad licenses.
        Use one line per BuildRequires/Requires/etc.
        Use %{version} instead of %{version}-%{release} for BuildRequires/etc.
        Remove AutoReqProv.
        Standardize BuildRoot.

        This one is a bit tricky since we reorder things. We have a notion of
        paragraphs, categories, and groups.

        A paragraph is a list of non-empty lines. Conditional directives like
        %if/%else/%endif also mark paragraphs. It contains categories.
        A category is a list of lines on the same topic. It contains a list of
        groups.
        A group is a list of lines where the first few ones are either %define
        or comment lines, and the last one is a normal line.

        This means that the %define and comments will stay attached to one
        line, even if we reorder the lines.
    """


    category_to_key = {
        'name': 'Name',
        'version': 'Version',
        'release': 'Release',
        'license': 'License',
        'summary': 'Summary',
        'url': 'Url',
        'group': 'Group',
        'source': 'Source',
        'patch': 'Patch',
        'buildrequires': 'BuildRequires',
        'prereq': 'Requires(pre)',
        'requires': 'Requires',
        'recommends': 'Recommends',
        'suggests': 'Suggests',
        'supplements': 'Supplements',
        # Provides/Obsoletes cannot be part of this since we want to keep them
        # mixed, so we'll have to specify the key when needed
        'buildroot': 'BuildRoot',
        'buildarch': 'BuildArch',
        'epoch': 'Epoch'
    }

    category_to_fixer = {
    }

    categories_order = [ 'define', 'name', 'version', 'release', 'license', 'summary', 'url', 'group', 'source', 'patch', 'buildrequires', 'prereq', 'requires', 'recommends', 'suggests', 'supplements', 'provides_obsoletes', 'buildroot', 'buildarch', 'misc' ]

    categories_with_sorted_package_tokens = [ 'buildrequires', 'prereq', 'requires', 'recommends', 'suggests', 'supplements' ]
    categories_with_package_tokens = categories_with_sorted_package_tokens[:]
    categories_with_package_tokens.append('provides_obsoletes')


    def __init__(self, specfile):
        Section.__init__(self, specfile)
        self.license_fixes = self._read_licenses_changes()
        self._start_paragraph()

        self.category_to_re = {
            'name': self.reg.re_name,
            'version': self.reg.re_version,
            'release': self.reg.re_release,
            'license': self.reg.re_license,
            'summary': self.reg.re_summary,
            'url': self.reg.re_url,
            'group': self.reg.re_group,
            # for source, we have a special match to keep the source number
            # for patch, we have a special match to keep the patch number
            'buildrequires': self.reg.re_buildrequires,
            'prereq': self.reg.re_prereq,
            'requires': self.reg.re_requires,
            'recommends': self.reg.re_recommends,
            'suggests': self.reg.re_suggests,
            'supplements': self.reg.re_supplements,
            # for provides/obsoletes, we have a special case because we group them
            # for build root, we have a special match because we force its value
            'buildarch': self.reg.re_buildarch,
            'epoch': self.reg.re_epoch
        }


    def _start_paragraph(self):
        self.paragraph = {}
        for i in self.categories_order:
            self.paragraph[i] = []
        self.current_group = []


    def _add_group(self, group):
        t = type(group)

        if t == str:
            Section.add(self, group)
        elif t == list:
            for subgroup in group:
                self._add_group(subgroup)
        else:
            raise RpmException('Unknown type of group in preamble: %s' % t)


    def _end_paragraph(self):
        def sort_helper_key(a):
            t = type(a)
            if t == str:
                key = a
            elif t == list:
                key = a[-1]
            else:
                raise RpmException('Unknown type during sort: %s' % t)

            # Put pkgconfig()-style packages at the end of the list, after all
            # non-pkgconfig()-style packages
            if key.find('pkgconfig(') != -1:
                return '1'+key
            else:
                return '0'+key

        for i in self.categories_order:
            if i in self.categories_with_sorted_package_tokens:
                self.paragraph[i].sort(key=sort_helper_key)
            for group in self.paragraph[i]:
                self._add_group(group)
        if self.current_group:
            # the current group was not added to any category. It's just some
            # random stuff that should be at the end anyway.
            self._add_group(self.current_group)

        self._start_paragraph()


    def _fix_license(self, value):
        # split using 'or', 'and' and parenthesis, ignore empty strings
        licenses = filter(lambda a: a != '', re.split('(\(|\)| and | or )', value))

        for (index, license) in enumerate(licenses):
            license = self.strip_useless_spaces(license)
            license = license.replace('ORlater','or later')
            license = license.replace('ORsim','or similar')
            if self.license_fixes.has_key(license):
                license = self.license_fixes[license]
            licenses[index] = license

        # create back new string with replaced licenses
        s = ' '.join(licenses).replace("( ","(").replace(" )",")")
        return [ s ]


    def _remove_tag(self, value):
        return []


    def _pkgname_to_pkgconfig(self, value):
        # conver the devel deps to pkgconfig ones
        files = FileUtils()
        files.open_datafile(PKGCONFIG_CONVERSIONS)

        r = {}
        for line in files.f:
            # the values are split by  ': '
            pair = line.split(': ')
            r[pair[0]] = pair[1][:-1]
        files.close()

        # we just want the pkgname if we have version string there
        # and for the pkgconfig deps we need to put the version into
        # the braces
        split = value.split()
        pkgname = value.split()[0]
        version = value.replace(pkgname,'')
        pkgconfig = []
        if not pkgname in r:
            # first check if the pacakge is in the replacements
            return [ value ]
        else:
            # first split the pkgconfig data
            pkgconf_list = r[pkgname].split()
            # then add each pkgconfig to the list
            #print pkgconf_list
            for j in pkgconf_list:
                pkgconfig.append('pkgconfig({0}){1}'.format(j, version))
        return pkgconfig


    def _fix_list_of_packages(self, value):
        if self.reg.re_requires_token.match(value):
            tokens = [ item[1] for item in self.reg.re_requires_token.findall(value) ]
            # first loop over all and do formatting as we can get more deps for one
            expanded = []
            for token in tokens:
                token = token.replace('%{version}-%{release}', '%{version}')
                # cleanup whitespace
                token = token.replace(' ','')
                # rpm actually allows ',' separated list of deps
                token = token.replace(',','')
                token = re.sub(r'([<>]=?|=)', r' \1 ', token)
                token = self._pkgname_to_pkgconfig(token)
                expanded += token
            # and then sort them :)
            expanded.sort()

            return expanded
        else:
            return [ value ]

    # fillup fixer the easy way
    category_to_fixer['license'] = _fix_license
    category_to_fixer['epoch'] = _remove_tag

    for i in categories_with_package_tokens:
        category_to_fixer[i] = _fix_list_of_packages


    def _add_line_value_to(self, category, value, key = None):
        """
            Change a key-value line, to make sure we have the right spacing.

            Note: since we don't have a key <-> category matching, we need to
            redo one. (Eg: Provides and Obsoletes are in the same category)
        """
        keylen = len('BuildRequires:  ')

        if key:
            pass
        elif self.category_to_key.has_key(category):
            key = self.category_to_key[category]
        else:
            raise RpmException('Unhandled category in preamble: %s' % category)

        key += ':'
        while len(key) < keylen:
            key += ' '

        if self.category_to_fixer.has_key(category):
            values = self.category_to_fixer[category](self, value)
        else:
            values = [ value ]

        # NOTE: _remove_tag relies on passing value = [] here
        for value in values:
            line = key + value
            self._add_line_to(category, line)


    def _add_line_to(self, category, line):
        if self.current_group:
            self.current_group.append(line)
            self.paragraph[category].append(self.current_group)
            self.current_group = []
        else:
            self.paragraph[category].append(line)

        self.previous_line = line


    def _read_licenses_changes(self):
        licenses = {}

        files = FileUtils()
        f = files.open_datafile(LICENSES_CHANGES)
        # ignore first line containing 'First line' (WTF?)
        files.f.readline()
        # load and store the rest
        for line in files.f:
            # strip newline
            line = line[:-1]
            # file has format
            # correct license string<tab>known bad license string
            # tab is used as separator
            pair = line.split('\t')
            licenses[pair[1]] = pair[0]
        files.close()
        return licenses


    def add(self, line):
        line = self._complete_cleanup(line)
        if len(line) == 0:
            if not self.previous_line or len(self.previous_line) == 0:
                return

            # we put the empty line in the current group (so we don't list it),
            # and write the paragraph
            self.current_group.append(line)
            self._end_paragraph()
            self.previous_line = line
            return

        elif self.reg.re_if.match(line):
            # %if/%else/%endif marks the end of the previous paragraph
            # We append the line at the end of the previous paragraph, though,
            # since it will stay at the end there. If putting it at the
            # beginning of the next paragraph, it will likely move (with the
            # misc category).
            self.current_group.append(line)
            self._end_paragraph()
            self.previous_line = line
            return

        elif self.reg.re_comment.match(line):
            self.current_group.append(line)
            self.previous_line = line
            return

        elif self.reg.re_define.match(line):
            match = self.reg.re_define.match(line)
            self._add_line_value_to('define', match.group(2), key = '%define%s' % match.group(1))
            return

        elif self.reg.re_autoreqprov.match(line):
            return

        elif self.reg.re_source.match(line):
            match = self.reg.re_source.match(line)
            self._add_line_value_to('source', match.group(2), key = 'Source%s' % match.group(1))
            return

        elif self.reg.re_patch.match(line):
            # FIXME: this is not perfect, but it's good enough for most cases
            if not self.previous_line or not self.reg.re_comment.match(self.previous_line):
                self.current_group.append('# PATCH-MISSING-TAG -- See http://wiki.opensuse.org/openSUSE:Packaging_Patches_guidelines')

            match = self.reg.re_patch.match(line)
            # convert Patch: to Patch0:
            if match.group(2) == '':
                zero = '0'
            else:
                zero = ''
            self._add_line_value_to('source', match.group(3), key = '%sPatch%s%s' % (match.group(1), zero, match.group(2)))
            return

        elif self.reg.re_provides.match(line):
            match = self.re_provides.match(line)
            self._add_line_value_to('provides_obsoletes', match.group(1), key = 'Provides')
            return

        elif self.reg.re_obsoletes.match(line):
            match = self.re_obsoletes.match(line)
            self._add_line_value_to('provides_obsoletes', match.group(1), key = 'Obsoletes')
            return

        elif self.reg.re_buildroot.match(line):
            if len(self.paragraph['buildroot']) == 0:
                self._add_line_value_to('buildroot', '%{_tmppath}/%{name}-%{version}-build')
            return

        else:
            for (category, regexp) in self.category_to_re.iteritems():
                match = regexp.match(line)
                if match:
                    # instead of matching first group as there is only one,
                    # take the last group
                    # (so I can have more advanced regexp for RPM tags)
                    self._add_line_value_to(category, match.groups()[len(match.groups()) - 1])
                    return

            self._add_line_to('misc', line)


    def output(self, fout):
        self._end_paragraph()
        Section.output(self, fout)


class RpmPackage(RpmPreamble):
    """
    We handle subpackage case as the normal preamble
    """


    def add(self, line):
        # The first line (%package) should always be added and is different
        # from the lines we handle in RpmPreamble.
        if self.previous_line is None:
            Section.add(self, line)
            return

        RpmPreamble.add(self, line)
