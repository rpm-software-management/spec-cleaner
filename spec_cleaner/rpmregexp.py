# vim: set ts=4 sw=4 et: coding=UTF-8

import re
import os

from fileutils import FileUtils


class RegexpSingle(object):
    """
        Singleton containing all regular expressions compiled in one run.
        So we can use them later everywhere without compiling them again,
    """

    # section macros
    re_spec_package = re.compile('^%package\s*', re.IGNORECASE)
    re_spec_description = re.compile('^%description\s*', re.IGNORECASE)
    re_spec_prep = re.compile('^%prep\s*$', re.IGNORECASE)
    re_spec_build = re.compile('^%build\s*$', re.IGNORECASE)
    re_spec_install = re.compile('^%install\s*$', re.IGNORECASE)
    re_spec_clean = re.compile('^%clean\s*$', re.IGNORECASE)
    re_spec_check = re.compile('^%check\s*$', re.IGNORECASE)
    re_spec_scriptlets = re.compile('(?:^%pretrans\s*)|(?:^%pre\s*)|(?:^%post\s*)|(?:^%preun\s*)|(?:^%postun\s*)|(?:^%posttrans\s*)', re.IGNORECASE)
    re_spec_files = re.compile('^%files\s*', re.IGNORECASE)
    re_spec_changelog = re.compile('^%changelog\s*$', re.IGNORECASE)

    # rpmpreamble
    re_if = re.compile('^\s*(?:%if\s|%ifarch\s|%ifnarch\s|%else\s*$|%endif\s*$)', re.IGNORECASE)
    re_name = re.compile('^Name:\s*(\S*)', re.IGNORECASE)
    re_version = re.compile('^Version:\s*(\S*)', re.IGNORECASE)
    re_release = re.compile('^Release:\s*(\S*)', re.IGNORECASE)
    re_license = re.compile('^License:\s*(.*)', re.IGNORECASE)
    re_summary = re.compile('^Summary:\s*([^\.]*).*', re.IGNORECASE)
    re_summary_localized = re.compile('^Summary(\(\S+\)):\s*([^\.]*).*', re.IGNORECASE)
    re_url = re.compile('^Url:\s*(\S*)', re.IGNORECASE)
    re_group = re.compile('^Group:\s*(.*)', re.IGNORECASE)
    re_vendor = re.compile('^Vendor:\s*(.*)', re.IGNORECASE)
    re_source = re.compile('^Source(\d*):\s*(\S*)', re.IGNORECASE)
    re_patch = re.compile('^((?:#[#\s]*)?)Patch(\d*):\s*(\S*)', re.IGNORECASE)
    re_buildrequires = re.compile('^BuildRequires:\s*(.*)', re.IGNORECASE)
    re_prereq = re.compile('^PreReq:\s*(.*)', re.IGNORECASE)
    re_requires = re.compile('^Requires:\s*(.*)', re.IGNORECASE)
    re_requires_phase = re.compile('^Requires(\(\S+\)):\s*(.*)', re.IGNORECASE)
    re_recommends = re.compile('^Recommends:\s*(.*)', re.IGNORECASE)
    re_suggests = re.compile('^Suggests:\s*(.*)', re.IGNORECASE)
    re_supplements = re.compile('^Supplements:\s*(.*)', re.IGNORECASE)
    re_provides = re.compile('^Provides:\s*(.*)', re.IGNORECASE)
    re_obsoletes = re.compile('^Obsoletes:\s*(.*)', re.IGNORECASE)
    re_buildroot = re.compile('^\s*BuildRoot:', re.IGNORECASE)
    re_buildarch = re.compile('^\s*BuildArch(itectures)?:\s*(.*)', re.IGNORECASE)
    re_epoch = re.compile('^\s*Epoch:\s*(.*)', re.IGNORECASE)
    re_define = re.compile('^\s*%define\s*(.*)', re.IGNORECASE)
    re_requires_token = re.compile('(\s*([\w_\-+\(\)%{}.]+(\s*[<>=]+\s*[\w_\-{}%.]+)?)\s*)')
    re_autoreqprov = re.compile('^\s*AutoReqProv:\s*on\s*$', re.IGNORECASE)
    # here we need to grab all submacros with rpm calls so just match almost everything
    re_rpm_command = re.compile('%\(rpm\s*')
    re_requires_eq = re.compile('^\s*%requires_eq\s*(.*)')

    # rpmbuild
    re_jobs = re.compile('%{(_smp_mflags|\?jobs:\s*-j\s*%(jobs|{jobs}))}')

    # rpmcopyright
    re_copyright = re.compile('^#\s*Copyright\ \(c\)\s*(.*)', re.IGNORECASE)
    re_suse_copyright = re.compile('SUSE LINUX Products GmbH, Nuernberg, Germany.\s*$', re.IGNORECASE)
    re_rootforbuild = re.compile('^#\s*needsrootforbuild\s*$', re.IGNORECASE)
    re_binariesforbuld = re.compile('^#\s*needsbinariesforbuild\s*$', re.IGNORECASE)
    re_nodebuginfo = re.compile('^#\s*nodebuginfo\s*$', re.IGNORECASE)
    re_icecream = re.compile('^#\s*icecream\s*$', re.IGNORECASE)

    # rpmfiles
    re_etcdir = re.compile('(^|\s)/etc/')
    re_usrdir = re.compile('(^|\s)/usr/')
    re_vardir = re.compile('(^|\s)/var/')
    re_dir = re.compile('^\s*%dir\s*(\S+)\s*')

    # rpminstall
    re_clean = re.compile('rm\s+(-?\w?\ ?)*"?(%{buildroot}|\$b)"?$')
    re_install = re.compile('{0}*(%make_install|%{{makeinstall}}|make{0}+install){0}*'.format('(DESTDIR=%{buildroot}|%{\?_smp_mflags}|\s|V=1|VERBOSE=1|-j\d+)'))
    re_rm = re.compile('rm\s+(-?\w?\ ?)*"?(%{buildroot}|\$b)"?/?"?%{_lib(dir)?}.+\.la;?$')
    re_find = re.compile('find\s+"?(%{buildroot}|\$b)("?\S?/?)*\s*.*\s+-i?name\s+["\'\\\\]?\*\.la($|.*[^\\\\]$)')
    re_find_double = re.compile('-i?name')
    re_rm_double = re.compile('(\.|{)a')

    # rpmprep
    re_patch_prep = re.compile('^%patch\s*([^P]*)-P\s*(\d*)\s*([^P]*)$')

    # comment detection
    re_comment = re.compile('^$|^\s*#')

    # macro detection
    re_macro = re.compile(r'(^|([^%]))%(\w+)(|(\W]))')

    # macro func detection
    re_spec_macrofunc = re.compile(r'^\s*%define\s(\w+)\(.*')


    # unbrace keywords love
    def _load_keywords_whitelist(self):
        """
        Create regexp for the unbrace keywords based on
        rpm showrc and whitelist.
        """

        BRACKETING_EXCLUDES = 'excludes-bracketing.txt'

        # load the keywords
        files = FileUtils()
        files.open_datafile(BRACKETING_EXCLUDES)
        keywords= []
        for line in files.f:
            keywords.append(line[:-1])
        files.close()

        return keywords


    def _parse_rpm_showrc(self):
        """
        Load argumented macros from rpm --showrc
        """

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

    def _find_macros_with_arg(self, spec):
        """
        Load argumented macros from specfile
        """

        macrofuncs = []

        files = FileUtils()
        files.open(spec, 'r')
        for line in files.f.readlines():
            line = line[:-1]
            found_macro = self.re_spec_macrofunc.sub(r'\1', line)
            if found_macro != line:
                macrofuncs += [ found_macro ]
        files.close()
        return macrofuncs

    def __init__(self, specfile):
        keywords = self._load_keywords_whitelist()
        global_macrofuncs = self._parse_rpm_showrc()
        spec_macrofuncs = self._find_macros_with_arg(specfile)

        self.re_unbrace_keywords = re.compile('%{(' + '|'.join(keywords + global_macrofuncs + spec_macrofuncs) + ')}')


    # singleton creation
    _instance = None


    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RegexpSingle, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance
