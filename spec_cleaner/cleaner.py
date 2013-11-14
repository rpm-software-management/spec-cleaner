# vim: set ts=4 sw=4 et: coding=UTF-8

import os
import sys
import cStringIO
import optparse
import re
import time
import tempfile
import subprocess
import shlex

from rpmsection import Section
from rpmexception import RpmException
from rpmcopyright import RpmCopyright

LICENSES_CHANGES = 'licenses_changes.txt'
PKGCONFIG_CONVERSIONS = 'pkgconfig_conversions.txt'
BRACKETING_EXCLUDES = 'excludes-bracketing.txt'

re_comment = re.compile('^$|^\s*#')
re_define = re.compile('^\s*%define', re.IGNORECASE)

re_bindir = re.compile('%{_prefix}/bin([/\s$])')
re_sbindir = re.compile('%{_prefix}/sbin([/\s$])')
re_includedir = re.compile('%{_prefix}/include([/\s$])')
re_datadir = re.compile('%{_prefix}/share([/\s$])')
re_mandir = re.compile('%{_datadir}/man([/\s$])')
re_infodir = re.compile('%{_datadir}/info([/\s$])')
re_docdir = re.compile('%{_datadir}/doc([/\s$])')

re_macro = re.compile(r'(^|([^%]))%(\w+)(|(\W]))')
re_jobs = re.compile('%{(_smp_mflags|\?jobs:\s*-j\s*%(jobs|{jobs}))}')

import re

def parse_rpm_showrc():
    macros = []
    re_rc_macrofunc = re.compile(r'^-[0-9]+[:=]\s(\w+)\(.*')
    output = os.popen('rpm --showrc')
    for line in output.readlines():
        line = line[:-1]
        found_macro = re_rc_macrofunc.sub(r'\1', line)
        if found_macro != line:
            macros += [ found_macro ]
    output.close()
    return macros

def open_datafile(FILE):
    try:
        f = open('/usr/share/spec-cleaner/{0}'.format(FILE), 'r')
    except IOError:
        # the .. is appended as we are in spec_cleaner sub_folder
        f = open('{0}/{1}'.format(os.path.dirname(os.path.realpath(__file__)) + '/../data/', FILE), 'r')

    return f


def strip_useless_spaces(s):
    return ' '.join(s.split())

def replace_known_dirs(s):
    s = s.replace('%{_usr}', '%{_prefix}')
    s = s.replace('%{_prefix}/%{_lib}', '%{_libdir}')
    # old typo in rpm macro
    s = s.replace('%_initrddir', '%{_initddir}')
    s = s.replace('%{_initrddir}', '%{_initddir}')

    s = re_bindir.sub(r'%{_bindir}\1', s)
    s = re_sbindir.sub(r'%{_sbindir}\1', s)
    s = re_includedir.sub(r'%{_includedir}\1', s)
    s = re_datadir.sub(r'%{_datadir}\1', s)
    s = re_mandir.sub(r'%{_mandir}\1', s)
    s = re_infodir.sub(r'%{_infodir}\1', s)
    s = re_docdir.sub(r'%{_docdir}\1', s)

    return s

def embrace_macros(s):
    # I don't think that this can be done within one regexp replacement
    # if you have idea, send me a patch :)

    # work only with non-commented part
    sp = s.split('#')
    # so, for now, put braces around everything, what looks like macro,
    sp[0] = re_macro.sub(r'\1%{\3}\4', sp[0])

    # and replace back known keywords to braceless state again
    sp[0] = re_unbrace_keywords.sub(r'%\1', sp[0])
    # re-create the line back
    return '#'.join(sp)

def replace_buildroot(s):
    s = s.replace('${RPM_BUILD_ROOT}', '%{buildroot}')
    s = s.replace('$RPM_BUILD_ROOT', '%{buildroot}')
    s = s.replace('%{buildroot}/etc/init.d/', '%{buildroot}%{_initddir}/')
    s = s.replace('%{buildroot}/etc/', '%{buildroot}%{_sysconfdir}/')
    s = s.replace('%{buildroot}/usr/', '%{buildroot}%{_prefix}/')
    s = s.replace('%{buildroot}/var/', '%{buildroot}%{_localstatedir}/')
    s = s.replace('"%{buildroot}"', '%{buildroot}')
    return s

def replace_optflags(s):
    s = s.replace('${RPM_OPT_FLAGS}', '%{optflags}')
    s = s.replace('$RPM_OPT_FLAGS', '%{optflags}')
    return s

def replace_remove_la(s):
    re_rm = re.compile('rm\s+(-?\w?\ ?)*"?(%{buildroot}|\$b)"?/?"?%{_lib(dir)?}.+\.la;?$')
    re_find = re.compile('find\s+"?(%{buildroot}|\$b)("?\S?/?)*\s*.*\s+-i?name\s+["\'\\\\]?\*\.la($|.*[^\\\\]$)')
    re_find_double = re.compile('-i?name')
    re_rm_double = re.compile('(\.|{)a')

    cmp_line = strip_useless_spaces(s)
    if (re_rm.search(cmp_line) and len(re_rm_double.split(cmp_line)) == 1) or ( re_find.search(cmp_line) and len(re_find_double.split(cmp_line)) == 2):
        s = 'find %{buildroot} -type f -name "*.la" -delete -print'
    return s

def replace_utils(s):
    # take care of all utilities macros that bloat spec file
    r = {'id_u': 'id -u', 'ln_s': 'ln -s', 'lzma': 'xz --format-lzma', 'mkdir_p': 'mkdir -p', 'awk':'gawk', 'cc':'gcc', 'cpp':'gcc -E', 'cxx':'g++', 'remsh':'rsh', }
    for i in r:
      s = s.replace('%{__' + i + '}', r[i])

    for i in [ 'aclocal', 'ar', 'as', 'autoconf', 'autoheader', 'automake', 'bzip2', 'cat', 'chgrp', 'chmod', 'chown', 'cp', 'cpio', 'file', 'gpg', 'grep', 'gzip', 'id', 'install', 'ld', 'libtoolize', 'make', 'mkdir', 'mv', 'nm', 'objcopy', 'objdump', 'patch', 'perl', 'python', 'ranlib', 'restorecon', 'rm', 'rsh', 'sed', 'semodule', 'ssh', 'strip', 'tar', 'unzip', 'xz', ]:
        s = s.replace('%{__' + i + '}', i)

    return s

def replace_buildservice(s):
    for i in ['centos', 'debian', 'fedora', 'mandriva', 'meego', 'rhel', 'sles', 'suse', 'ubuntu']:
        s = s.replace('%{' + i + '_version}', '0%{?' + i + '_version}').replace('00%{','0%{')
    return s

def replace_preamble_macros(s):
    for i in map(str,range(100)):
        s = s.replace('%{P:' + i + '}', '%{PATCH' + i + '}')
        s = s.replace('%{S:' + i + '}', '%{SOURCE' + i + '}')
    return s

def read_licenses_changes():
    licenses = {}

    f = open_datafile(LICENSES_CHANGES)
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

def replace_all(s):
    s = embrace_macros(s)
    s = replace_buildroot(s)
    s = replace_optflags(s)
    s = replace_known_dirs(s)
    s = replace_utils(s)
    s = replace_buildservice(s)
    s = replace_preamble_macros(s)
    s = replace_remove_la(s)
    return s

#######################################################################



#######################################################################


class RpmPreamble(Section):
    '''
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
    '''

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

    license_fixes = read_licenses_changes()

    categories_order = [ 'name', 'version', 'release', 'license', 'summary', 'url', 'group', 'source', 'patch', 'buildrequires', 'prereq', 'requires', 'recommends', 'suggests', 'supplements', 'provides_obsoletes', 'buildroot', 'buildarch', 'misc' ]

    categories_with_sorted_package_tokens = [ 'buildrequires', 'prereq', 'requires', 'recommends', 'suggests', 'supplements' ]
    categories_with_package_tokens = categories_with_sorted_package_tokens[:]
    categories_with_package_tokens.append('provides_obsoletes')

    re_autoreqprov = re.compile('^\s*AutoReqProv:\s*on\s*$', re.IGNORECASE)


    def __init__(self):
        Section.__init__(self)
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
            license = strip_useless_spaces(license)
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
        f = open_datafile(PKGCONFIG_CONVERSIONS)

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

        elif re_comment.match(line) or re_define.match(line):
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
            if not self.previous_line or not re_comment.match(self.previous_line):
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


    def output(self, fout):
        self._end_paragraph()
        Section.output(self, fout)


#######################################################################





#######################################################################


class RpmDescription(Section):
    '''
        Only keep one empty line for many consecutive ones.
        Remove Authors from description.
    '''

    def __init__(self):
        Section.__init__(self)
        self.removing_authors = False
        # Tracks the use of a macro. When this happens and we're still in a
        # description, we actually don't know where we are so we just put all
        # the following lines blindly, without trying to fix anything.
        self.unknown_line = False

    def add(self, line):
        lstrip = line.lstrip()
        if self.previous_line != None and len(lstrip) > 0 and lstrip[0] == '%':
            self.unknown_line = True

        if self.removing_authors and not self.unknown_line:
            return

        if len(line) == 0:
            if not self.previous_line or len(self.previous_line) == 0:
                return

        if line == 'Authors:':
            self.removing_authors = True
            return

        Section.add(self, line)


#######################################################################


class RpmPrep(Section):
    '''
        Try to simplify to %setup -q when possible.
        Replace %patch with %patch0
    '''

    re_patch = re.compile('^%patch\s*(.*)-P\s*(\d*)\s*(.*)')

    def add(self, line):
        if line.startswith('%setup'):
            cmp_line = line.replace(' -q', '')
            cmp_line = cmp_line.replace(' -n %{name}-%{version}', '')
            line = strip_useless_spaces(cmp_line)

        if self.re_patch.match(line):
            match = self.re_patch.match(line)
            line = strip_useless_spaces('%%patch%s %s %s' % (match.group(2), match.group(1), match.group(3)))
        elif line.startswith('%patch ') or line == '%patch':
            line = line.replace('%patch','%patch0')

        line = embrace_macros(line)
        Section.add(self, line)


#######################################################################


class RpmBuild(Section):
    '''
        Replace %{?jobs:-j%jobs} (suse-ism) with %{?_smp_mflags}
    '''

    def add(self, line):
        if not re_comment.match(line):
            line = embrace_macros(line)
        line = re_jobs.sub('%{?_smp_mflags}', line)

        Section.add(self, line)


#######################################################################


class RpmInstall(Section):
    '''
        Remove commands that wipe out the build root.
        Use %make_install macro.
        Replace %makeinstall (suse-ism).
    '''

    def add(self, line):
        # remove double spaces when comparing the line
        cmp_line = strip_useless_spaces(line)
        cmp_line = embrace_macros(cmp_line)
        cmp_line = replace_buildroot(cmp_line)

        # FIXME: this is very poor patching
        if cmp_line.find('DESTDIR=%{buildroot}') != -1:
            buf = cmp_line.replace('DESTDIR=%{buildroot}', '')
            buf = strip_useless_spaces(buf)
            if buf == 'make install' or buf == 'make  install':
                line = '%make_install'
        elif cmp_line == '%{makeinstall}':
            line = '%make_install'
        elif cmp_line == 'rm -rf %{buildroot}':
            return

        Section.add(self, line)


#######################################################################


class RpmClean(Section):
    '''
        Remove clean section
    '''

    def output(self, fout):
        pass


#######################################################################


class RpmScriptlets(Section):
    '''
        Do %post -p /sbin/ldconfig when possible.
    '''

    def __init__(self):
        Section.__init__(self)
        self.cache = []


    def add(self, line):
        if len(self.lines) == 0:
            if not self.cache:
                if line.find(' -p ') == -1 and line.find(' -f ') == -1:
                    self.cache.append(line)
                    return
            else:
                if line in ['', '/sbin/ldconfig' ]:
                    self.cache.append(line)
                    return
                else:
                    for cached in self.cache:
                        Section.add(self, cached)
                    self.cache = None

        Section.add(self, line)


    def output(self, fout):
        if self.cache:
            Section.add(self, self.cache[0] + ' -p /sbin/ldconfig')
            Section.add(self, '')

        Section.output(self, fout)


#######################################################################


class RpmFiles(Section):
    """
        Replace additional /usr, /etc and /var because we're sure we can use
        macros there.

        Replace '%dir %{_includedir}/mux' and '%{_includedir}/mux/*' with
        '%{_includedir}/mux/'
    """

    re_etcdir = re.compile('(^|\s)/etc/')
    re_usrdir = re.compile('(^|\s)/usr/')
    re_vardir = re.compile('(^|\s)/var/')

    re_dir = re.compile('^\s*%dir\s*(\S+)\s*')

    def __init__(self):
        Section.__init__(self)
        self.dir_on_previous_line = None


    def add(self, line):
        line = self.re_etcdir.sub(r'\1%{_sysconfdir}/', line)
        line = self.re_usrdir.sub(r'\1%{_prefix}/', line)
        line = self.re_vardir.sub(r'\1%{_localstatedir}/', line)

        if self.dir_on_previous_line:
            if line == self.dir_on_previous_line + '/*':
                Section.add(self, self.dir_on_previous_line + '/')
                self.dir_on_previous_line = None
                return
            else:
                Section.add(self, '%dir ' + self.dir_on_previous_line)
                self.dir_on_previous_line = None

        match = self.re_dir.match(line)
        if match:
            self.dir_on_previous_line = match.group(1)
            return

        Section.add(self, line)


#######################################################################


class RpmChangelog(Section):
    '''
        Remove changelog entries.
    '''

    def add(self, line):
        # only add the first line (%changelog)
        if len(self.lines) == 0:
            Section.add(self, line)


#######################################################################


class RpmPackage(RpmPreamble):
    '''
        We handle this the same was as the preamble.
    '''

    def add(self, line):
        # The first line (%package) should always be added and is different
        # from the lines we handle in RpmPreamble.
        if self.previous_line is None:
            Section.add(self, line)
            return

        RpmPreamble.add(self, line)

class RpmSpecCleaner:
    specfile = None
    fin = None
    fout = None
    current_section = None

    re_spec_package = re.compile('^%package\s*', re.IGNORECASE)
    re_spec_description = re.compile('^%description\s*', re.IGNORECASE)
    re_spec_prep = re.compile('^%prep\s*$', re.IGNORECASE)
    re_spec_build = re.compile('^%build\s*$', re.IGNORECASE)
    re_spec_install = re.compile('^%install\s*$', re.IGNORECASE)
    re_spec_clean = re.compile('^%clean\s*$', re.IGNORECASE)
    re_spec_scriptlets = re.compile('(?:^%pretrans\s*)|(?:^%pre\s*)|(?:^%post\s*)|(?:^%preun\s*)|(?:^%postun\s*)|(?:^%posttrans\s*)', re.IGNORECASE)
    re_spec_files = re.compile('^%files\s*', re.IGNORECASE)
    re_spec_changelog = re.compile('^%changelog\s*$', re.IGNORECASE)

    re_spec_macrofunc = re.compile(r'^\s*%define\s(\w+)\(.*')

    section_starts = [
        (re_spec_package, RpmPackage),
        (re_spec_description, RpmDescription),
        (re_spec_prep, RpmPrep),
        (re_spec_build, RpmBuild),
        (re_spec_install, RpmInstall),
        (re_spec_clean, RpmClean),
        (re_spec_scriptlets, RpmScriptlets),
        (re_spec_files, RpmFiles),
        (re_spec_changelog, RpmChangelog)
    ]


    def __init__(self, specfile, output, inline, diff, diff_prog):
        self.specfile = specfile
        self.output = output
        self.inline = inline
        self.diff = diff
        self.diff_prog = diff_prog

        global global_macrofuncs
        global_macrofuncs = parse_rpm_showrc()
        glob_macrofuncs = global_macrofuncs

        spec_macrofuncs = self.find_macros_with_arg(specfile)

        f = open_datafile(BRACKETING_EXCLUDES)

        keywords= []
        for line in f:
            keywords.append(line[:-1])

        global re_unbrace_keywords
        re_unbrace_keywords = re.compile('%{(' + '|'.join(keywords + glob_macrofuncs + spec_macrofuncs) + ')}')

        self.fin = open(self.specfile)

        if self.output:
            self.fout = open(self.output, 'w')
        elif self.inline:
            io = cStringIO.StringIO()
            while True:
                bytes = self.fin.read(500 * 1024)
                if len(bytes) == 0:
                    break
                io.write(bytes)

            self.fin.close()
            io.seek(0)
            self.fin = io
            self.fout = open(self.specfile, 'w')
        elif self.diff:
            self.fout = tempfile.NamedTemporaryFile(prefix=self.specfile+'.', suffix='.spec')
        else:
            self.fout = sys.stdout


    def run(self):
        if not self.specfile or not self.fin:
            raise RpmException('No spec file.')


        def _line_for_new_section(self, line):
            if isinstance(self.current_section, RpmCopyright):
                if not re_comment.match(line):
                    return RpmPreamble

            for (regexp, newclass) in self.section_starts:
                if regexp.match(line):
                    return newclass

            return None


        self.current_section = RpmCopyright(self.specfile)

        while True:
            line = self.fin.readline()
            if len(line) == 0:
                break
            # Remove \n to make it easier to parse things
            line = line[:-1]

            new_class = _line_for_new_section(self, line)
            if new_class:
                self.current_section.output(self.fout)
                self.current_section = new_class()

            self.current_section.add(line)

        self.current_section.output(self.fout)
        self.fout.flush()

        if self.diff:
            cmd = shlex.split(self.diff_prog + " " + self.specfile.replace(" ","\\ ") + " " + self.fout.name.replace(" ","\\ "))
            try:
                subprocess.call(cmd, shell=False)
            except OSError as e:
                raise RpmException('Could not execute %s (%s)' % (self.diff_prog.split()[0], e.strerror))

    def find_macros_with_arg(self, spec):
        macrofuncs = []
        specfile = open(spec, 'r')
        for line in specfile.readlines():
            line = line[:-1]
            found_macro = self.re_spec_macrofunc.sub(r'\1', line)
            if found_macro != line:
                macrofuncs += [ found_macro ]
        specfile.close()
        return macrofuncs

    def __del__(self):
        if self.fin:
            self.fin.close()
            self.fin = None
        if self.fout:
            self.fout.close()
            self.fout = None
