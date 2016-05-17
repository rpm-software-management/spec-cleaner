# vim: set ts=4 sw=4 et: coding=UTF-8

import re
import os

from .fileutils import FileUtils


class Singleton(object):

    def __init__(self, klass):
        self.klass = klass
        self.instance = None

    def __call__(self, *args, **kwds):
        if self.instance is None:
            self.instance = self.klass(*args, **kwds)
        return self.instance


@Singleton
class RegexpSingle(object):

    """
        Singleton containing all regular expressions compiled in one run.
        So we can use them later everywhere without compiling them again,
    """

    # section macros
    re_spec_package = re.compile(r'^%package(\s+|$)', re.IGNORECASE)
    re_spec_description = re.compile(r'^%description(\s+|$)', re.IGNORECASE)
    re_spec_prep = re.compile(r'^%prep\s*$', re.IGNORECASE)
    re_spec_build = re.compile(r'^%build\s*$', re.IGNORECASE)
    re_spec_install = re.compile(r'^%install\s*$', re.IGNORECASE)
    re_spec_clean = re.compile(r'^%clean\s*$', re.IGNORECASE)
    re_spec_check = re.compile(r'^%check\s*$', re.IGNORECASE)
    re_spec_scriptlets = re.compile(r'(?:^%pretrans(\s+|$))|(?:^%pre(\s+|$))|(?:^%post(\s+|$))|(?:^%verifyscript(\s+|$))|(?:^%preun(\s+|$))|(?:^%postun(\s+|$))|(?:^%posttrans(\s+|$))', re.IGNORECASE)
    re_spec_files = re.compile(r'^%files(\s+|$)', re.IGNORECASE)
    re_spec_changelog = re.compile(r'^%changelog\s*$', re.IGNORECASE)

    # rpmpreamble
    # WARNING: keep in sync with rpmcleaner Section change detection
    re_if = re.compile(r'^\s*(?:%{?if\s|%{?ifarch\s|%{?ifnarch\s)', re.IGNORECASE)
    re_else = re.compile(r'^\s*%else(\s.*|)$', re.IGNORECASE)
    re_endif = re.compile(r'^\s*%endif(\s.*|)$', re.IGNORECASE)
    re_name = re.compile(r'^Name:\s*(\S*)', re.IGNORECASE)
    re_version = re.compile(r'^Version:\s*(.*)', re.IGNORECASE)
    re_release = re.compile(r'^Release:\s*(\S*)', re.IGNORECASE)
    re_license = re.compile(r'^License:\s*(.*)', re.IGNORECASE)
    re_summary = re.compile(r'^Summary:\s*(.*)', re.IGNORECASE)
    re_summary_localized = re.compile(r'^Summary(\(\S+\)):\s*(.*)', re.IGNORECASE)
    re_url = re.compile(r'^Url:\s*(\S*)', re.IGNORECASE)
    re_group = re.compile(r'^Group:\s*(.*)', re.IGNORECASE)
    re_vendor = re.compile(r'^Vendor:\s*(.*)', re.IGNORECASE)
    re_source = re.compile(r'^Source(\d*):\s*(\S*)', re.IGNORECASE)
    re_nosource = re.compile(r'^NoSource:\s*(.*)', re.IGNORECASE)
    re_patch = re.compile(r'^((?:#[#\s]*)?)Patch(\d*):\s*(\S*)', re.IGNORECASE)
    re_buildrequires = re.compile(r'^BuildRequires:\s*(.*)', re.IGNORECASE)
    re_prereq = re.compile(r'^PreReq:\s*(.*)', re.IGNORECASE)
    re_requires = re.compile(r'^Requires:\s*(.*)', re.IGNORECASE)
    re_requires_phase = re.compile(r'^Requires(\(\S+\)):\s*(.*)', re.IGNORECASE)
    re_recommends = re.compile(r'^Recommends:\s*(.*)', re.IGNORECASE)
    re_suggests = re.compile(r'^Suggests:\s*(.*)', re.IGNORECASE)
    re_enhances = re.compile(r'^Enhances:\s*(.*)', re.IGNORECASE)
    re_supplements = re.compile(r'^Supplements:\s*(.*)', re.IGNORECASE)
    re_conflicts = re.compile(r'^Conflicts:\s*(.*)', re.IGNORECASE)
    re_provides = re.compile(r'^Provides:\s*(.*)', re.IGNORECASE)
    re_obsoletes = re.compile(r'^Obsoletes:\s*(.*)', re.IGNORECASE)
    re_buildroot = re.compile(r'^\s*BuildRoot:', re.IGNORECASE)
    re_buildarch = re.compile(r'^\s*BuildArch(itectures)?:\s*(.*)', re.IGNORECASE)
    re_epoch = re.compile(r'^\s*Epoch:\s*(.*)', re.IGNORECASE)
    re_icon = re.compile(r'^\s*Icon:\s*(.*)', re.IGNORECASE)
    re_copyright = re.compile(r'^\s*Copyright:\s*(.*)', re.IGNORECASE)
    re_packager = re.compile(r'^\s*Packager:\s*(.*)', re.IGNORECASE)
    re_define = re.compile(r'^\s*%define\s*(.*)', re.IGNORECASE)
    re_global = re.compile(r'^\s*%global\s*(.*)', re.IGNORECASE)
    re_bcond_with = re.compile(r'^\s*%bcond_with(out)?\s*(.*)', re.IGNORECASE)
    re_requires_token = re.compile(r'(\s*([^<>=\s]+(\s*[<>=]+\s*[^<>=\s]+)?)\s*)')
    re_autoreqprov = re.compile(r'^\s*AutoReqProv:.*$', re.IGNORECASE)
    re_debugpkg = re.compile(r'^%{?(debug_package|___debug_install_post)}?\s*$', re.IGNORECASE)
    re_preamble_prefix = re.compile(r'^Prefix:\s*(.*)', re.IGNORECASE)
    # here we need to grab all submacros with rpm calls so just match almost
    # everything
    re_rpm_command = re.compile(r'%\(.*\)')
    re_requires_eq = re.compile(r'^\s*%requires_eq\s*(.*)')
    re_onelinecond = re.compile(r'^\s*%{!?[^?]*\?[^:]+:[^}]+}')
    # license ; should be replaced by ands so find it
    re_license_semicolon = re.compile(r'\s*;\s*')

    # rpmdescription
    re_authors = re.compile(r'^\s*Author(s)?:\s*')

    # rpmbuild
    re_jobs = re.compile(r'%{?(_smp_mflags|\?_smp_flags|\?jobs:\s*-j\s*%(jobs|{jobs}))}?')
    re_make = re.compile(r'(^|(.*\s)?)make($|(\s.*)?)')
    re_optflags_quotes = re.compile(r'=\s*\${?RPM_OPT_FLAGS}?\s*$')
    re_optflags = re.compile(r'\${?RPM_OPT_FLAGS}?')
    re_suseupdateconfig = re.compile(r'(%{?suse_update_config|${?\?suse_update_config:)')

    # rpmcopyright
    re_copyright = re.compile(r'^#\s*Copyright\ \(c\)\s*(.*)', re.IGNORECASE)
    re_suse_copyright = re.compile(r'SUSE LINUX (Products )?GmbH, Nuernberg, Germany.\s*$', re.IGNORECASE)
    re_rootforbuild = re.compile(r'^#\s*needsrootforbuild\s*$', re.IGNORECASE)
    re_binariesforbuld = re.compile(r'^#\s*needsbinariesforbuild\s*$', re.IGNORECASE)
    re_nodebuginfo = re.compile(r'^#\s*nodebuginfo\s*$', re.IGNORECASE)
    re_sslcerts = re.compile(r'^#\s*needssslcertforbuild\s*$', re.IGNORECASE)
    re_icecream = re.compile(r'^#\s*icecream\s*$', re.IGNORECASE)
    re_vimmodeline = re.compile(r'^# vim:', re.IGNORECASE)

    # rpminstall
    re_clean = re.compile(r'rm\s+(-?\w?\ ?)*"?(%{buildroot}|\$b)"?$')
    re_install = re.compile(r'{0}*(%{{makeinstall}}|make{0}+install){0}*$'.format(r'(DESTDIR=%{buildroot}|%{\?_smp_mflags}|\s|V=1|VERBOSE=1|-j\d+)'))
    re_rm = re.compile(r'rm\s+(-?\w?\ ?)*"?(%{buildroot}|\$b)"?/?"?%{_lib(dir)?}.*\*\.la;?$')
    re_find = re.compile(r'find\s+"?(%{buildroot}|\$b)("?\S?/?)*\s*.*\s+-i?name\s+["\'\\\\]?\*\.la($|.*[^\\\\]$)')
    re_find_double = re.compile(r'-i?name')
    re_rm_double = re.compile(r'(\.|{)a')

    # rpmprep
    re_patch_prep = re.compile(r'^%patch\s*([^P]*)-P\s*(\d*)\s*([^P]*)$')
    re_setup = re.compile(r'\s*-n\s+"?%{name}-%{version}"?($|\s)')

    # rpmfiles
    re_compression = re.compile(r'\.(gz|\*)$')

    # patches/sources
    re_ptch = re.compile(r'%{P:(\d+)}')
    re_src = re.compile(r'%{S:(\d+)}')

    # comment detection
    re_comment = re.compile(r'^$|^\s*#')

    # macro detection
    re_macro = re.compile(r'(^|([^%]))%([1-9]\d*|[a-zA-Z_]\w*(\s*\([^)]*\))?)(|(\W))')
    # macro func detection
    re_spec_macrofunc = re.compile(r'^\s*%define\s(\w+)\(.*')

    # cleaning path regexps
    re_oldprefix = re.compile(r'%{?_exec_prefix}?([/\s$])')
    re_prefix = re.compile(r'(?<!\w)/usr(/|\s|$)')
    re_bindir = re.compile(r'%{?_prefix}?/bin([/\s$])')
    re_sbindir = re.compile(r'%{?_prefix}?/sbin([/\s$])')
    re_libexecdir = re.compile(r'%{?_prefix}?/lib([/\s$])')
    re_includedir = re.compile(r'%{?_prefix}?/include([/\s$])')
    re_datadir = re.compile(r'%{?_prefix}?/share([/\s$])')
    re_mandir = re.compile(r'%{?_datadir}?/man([/\s$])')
    re_infodir = re.compile(r'%{?_datadir}?/info([/\s$])')
    re_docdir = re.compile(r'%{?_datadir}?/doc/packages([/\s$])')
    re_initdir = re.compile(r'/etc/init.d([/\s$])')
    re_sysconfdir = re.compile(r'/etc([/\s$])')
    re_localstatedir = re.compile(r'/var([/\s$])')
    re_libdir = re.compile(r'%{?_prefix}?/(%{?_lib}?|lib64)([/\s$])')
    re_initddir = re.compile(r'%{?_initrddir}?([/\s$])')
    re_rpmbuildroot = re.compile(r'(\${?RPM_BUILD_ROOT}?|"%{?buildroot}?")([/\s%]|$)')
    re_rpmbuildroot_quotes = re.compile(r'"\${?RPM_BUILD_ROOT}?"')

    def _load_keywords_whitelist(self):
        """
        Create regexp for the unbrace keywords based on
        rpm showrc and whitelist.
        """

        BRACKETING_EXCLUDES = 'excludes-bracketing.txt'

        # load the keywords
        files = FileUtils()
        files.open_datafile(BRACKETING_EXCLUDES)
        keywords = []
        for line in files.f:
            keywords.append(line.rstrip('\n'))
        files.close()

        return keywords

    def _parse_rpm_showrc(self):
        """
        Load argumented macros from rpm --showrc
        """

        macros = []
        re_rc_macrofunc = re.compile(r'^-[0-9]+[:=]\s(\w+)\(.*')
        output = os.popen('rpm --showrc')
        for line in output:
            line = line.rstrip('\n')
            found_macro = re_rc_macrofunc.sub(r'\1', line)
            if found_macro != line:
                macros += [found_macro]
        output.close()
        return macros

    def _find_macros_with_arg(self, spec):
        """
        Load argumented macros from specfile
        """

        macrofuncs = []

        files = FileUtils()
        files.open(spec, 'r')
        for line in files.f:
            line = line.rstrip('\n')
            found_macro = self.re_spec_macrofunc.sub(r'\1', line)
            if found_macro != line:
                macrofuncs += [found_macro]
        files.close()
        return macrofuncs

    def __init__(self, specfile):
        keywords = self._load_keywords_whitelist()
        global_macrofuncs = self._parse_rpm_showrc()
        spec_macrofuncs = self._find_macros_with_arg(specfile)
        self.re_unbrace_keywords = re.compile('%{(' + '|'.join(keywords + global_macrofuncs + spec_macrofuncs) + ')}')
