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

    re_if = re.compile('^\s*(?:%if\s|%ifarch\s|%ifnarch\s|%else\s*$|%endif\s*$)', re.IGNORECASE)

    re_name = re.compile('^Name:\s*(\S*)', re.IGNORECASE)
    re_version = re.compile('^Version:\s*(\S*)', re.IGNORECASE)
    re_release = re.compile('^Release:\s*(\S*)', re.IGNORECASE)
    re_license = re.compile('^License:\s*(.*)', re.IGNORECASE)
    re_summary = re.compile('^Summary:\s*([^\.]*).*', re.IGNORECASE)
    re_url = re.compile('^Url:\s*(\S*)', re.IGNORECASE)
    re_group = re.compile('^Group:\s*(.*)', re.IGNORECASE)
    re_source = re.compile('^Source(\d*):\s*(\S*)', re.IGNORECASE)
    re_patch = re.compile('^((?:#[#\s]*)?)Patch(\d*):\s*(\S*)', re.IGNORECASE)
    re_buildrequires = re.compile('^BuildRequires:\s*(.*)', re.IGNORECASE)
    re_prereq = re.compile('^PreReq:\s*(.*)', re.IGNORECASE)
    re_requires = re.compile('^Requires:\s*(.*)', re.IGNORECASE)
    re_recommends = re.compile('^Recommends:\s*(.*)', re.IGNORECASE)
    re_suggests = re.compile('^Suggests:\s*(.*)', re.IGNORECASE)
    re_supplements = re.compile('^Supplements:\s*(.*)', re.IGNORECASE)
    re_provides = re.compile('^Provides:\s*(.*)', re.IGNORECASE)
    re_obsoletes = re.compile('^Obsoletes:\s*(.*)', re.IGNORECASE)
    re_buildroot = re.compile('^\s*BuildRoot:', re.IGNORECASE)
    re_buildarch = re.compile('^\s*BuildArch(itectures)?:\s*(.*)', re.IGNORECASE)
    re_epoch = re.compile('^\s*Epoch:\s*(.*)', re.IGNORECASE)
    re_define = re.compile('^\s*%define', re.IGNORECASE)
    re_comment = re.compile('^$|^\s*#')

    re_requires_token = re.compile('(\s*(\S+(?:\s*(?:[<>]=?|=)\s*[^\s,]+)?),?)')

    category_to_re = {
        'name': re_name,
        'version': re_version,
        'release': re_release,
        'license': re_license,
        'summary': re_summary,
        'url': re_url,
        'group': re_group,
        # for source, we have a special match to keep the source number
        # for patch, we have a special match to keep the patch number
        'buildrequires': re_buildrequires,
        'prereq': re_prereq,
        'requires': re_requires,
        'recommends': re_recommends,
        'suggests': re_suggests,
        'supplements': re_supplements,
        # for provides/obsoletes, we have a special case because we group them
        # for build root, we have a special match because we force its value
        'buildarch': re_buildarch,
        'epoch': re_epoch
    }

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

    categories_order = [ 'name', 'version', 'release', 'license', 'summary', 'url', 'group', 'source', 'patch', 'buildrequires', 'prereq', 'requires', 'recommends', 'suggests', 'supplements', 'provides_obsoletes', 'buildroot', 'buildarch', 'misc' ]

    categories_with_sorted_package_tokens = [ 'buildrequires', 'prereq', 'requires', 'recommends', 'suggests', 'supplements' ]
    categories_with_package_tokens = categories_with_sorted_package_tokens[:]
    categories_with_package_tokens.append('provides_obsoletes')

    re_autoreqprov = re.compile('^\s*AutoReqProv:\s*on\s*$', re.IGNORECASE)


    def __init__(self, re_unbrace_keywords):
        Section.__init__(self, re_unbrace_keywords)
        self.license_fixes = self.read_licenses_changes()
        self._start_paragraph()


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
            license = license.replace('ORlater','or later').replace('ORsim','or similar')
            if self.license_fixes.has_key(license):
                license = self.license_fixes[license]
            licenses[index] = license

        # create back new string with replaced licenses
        s = ' '.join(licenses).replace("( ","(").replace(" )",")")
        return [ s ]

    category_to_fixer['license'] = _fix_license

    def _remove_tag(self, value):
        return []

    category_to_fixer['epoch'] = _remove_tag

    def _pkgname_to_pkgconfig(self, value):
        # conver the devel deps to pkgconfig ones
        files = FileUtils()
        f = files.open_datafile(PKGCONFIG_CONVERSIONS)

        r = {}
        for line in f:
            # the values are split by  ': '
            pair = line.split(': ')
            r[pair[0]] = pair[1][:-1]

        for i in r:
            value = value.replace(i, 'pkgconfig('+r[i]+')')
        return value

    def _fix_list_of_packages(self, value):
        if self.re_requires_token.match(value):
            tokens = [ item[1] for item in self.re_requires_token.findall(value) ]
            for (index, token) in enumerate(tokens):
                token = token.replace('%{version}-%{release}', '%{version}')
                token = token.replace(' ','')
                token = re.sub(r'([<>]=?|=)', r' \1 ', token)
                token = self._pkgname_to_pkgconfig(token)
                tokens[index] = token

            tokens.sort()
            return tokens
        else:
            return [ value ]

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


    def add(self, line):
        if len(line) == 0:
            if not self.previous_line or len(self.previous_line) == 0:
                return

            # we put the empty line in the current group (so we don't list it),
            # and write the paragraph
            self.current_group.append(line)
            self._end_paragraph()
            self.previous_line = line
            return

        elif self.re_if.match(line):
            # %if/%else/%endif marks the end of the previous paragraph
            # We append the line at the end of the previous paragraph, though,
            # since it will stay at the end there. If putting it at the
            # beginning of the next paragraph, it will likely move (with the
            # misc category).
            self.current_group.append(line)
            self._end_paragraph()
            self.previous_line = line
            return

        elif self.re_comment.match(line) or self.re_define.match(line):
            self.current_group.append(line)
            self.previous_line = line
            return

        elif self.re_autoreqprov.match(line):
            return

        elif self.re_source.match(line):
            match = self.re_source.match(line)
            self._add_line_value_to('source', match.group(2), key = 'Source%s' % match.group(1))
            return

        elif self.re_patch.match(line):
            # FIXME: this is not perfect, but it's good enough for most cases
            if not self.previous_line or not self.re_comment.match(self.previous_line):
                self.current_group.append('# PATCH-MISSING-TAG -- See http://wiki.opensuse.org/openSUSE:Packaging_Patches_guidelines')

            match = self.re_patch.match(line)
            # convert Patch: to Patch0:
            if match.group(2) == '':
                zero = '0'
            else:
                zero = ''
            self._add_line_value_to('source', match.group(3), key = '%sPatch%s%s' % (match.group(1), zero, match.group(2)))
            return

        elif self.re_provides.match(line):
            match = self.re_provides.match(line)
            self._add_line_value_to('provides_obsoletes', match.group(1), key = 'Provides')
            return

        elif self.re_obsoletes.match(line):
            match = self.re_obsoletes.match(line)
            self._add_line_value_to('provides_obsoletes', match.group(1), key = 'Obsoletes')
            return

        elif self.re_buildroot.match(line):
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

    def read_licenses_changes(self):
        licenses = {}

        files = FileUtils()
        f = files.open_datafile(LICENSES_CHANGES)
        # ignore first line containing 'First line' (WTF?)
        f.readline()
        # load and store the rest
        for line in f:
            # strip newline
            line = line[:-1]
            # file has format
            # correct license string<tab>known bad license string
            # tab is used as separator
            pair = line.split('\t')
            licenses[pair[1]] = pair[0]
        return licenses



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
