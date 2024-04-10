# vim: set ts=4 sw=4 et: coding=UTF-8

import re
from typing import List


class Regexp(object):
    """
    Singleton containing all regular expressions compiled in one run.

    So we can use them later everywhere without compiling them again.
    """

    # section macros
    re_spec_package = re.compile(r'^%package(\s+|$)', re.IGNORECASE)
    re_spec_description = re.compile(r'^%description(\s+|$)', re.IGNORECASE)
    re_spec_prep = re.compile(r'^%prep\s*$', re.IGNORECASE)
    re_spec_build = re.compile(r'^%build\s*$', re.IGNORECASE)
    re_spec_install = re.compile(r'^%install\s*$', re.IGNORECASE)
    re_spec_clean = re.compile(r'^%clean\s*$', re.IGNORECASE)
    re_spec_check = re.compile(r'^%check\s*$', re.IGNORECASE)
    re_spec_scriptlets = re.compile(
        r'(?:^%pretrans(\s+|$))|(?:^%pre(\s+|$))|(?:^%post(\s+|$))|(?:^%verifyscript(\s+|$))|(?:^%preun(\s+|$))|(?:^%postun(\s+|$))|(?:^%posttrans(\s+|$))',
        re.IGNORECASE,
    )
    re_spec_triggers = re.compile(
        r'(?:^%filetriggerin(\s+|$))|(?:^%filetriggerun(\s+|$))|(?:^%filetriggerpostun(\s+|$))|(?:^%transfiletriggerin(\s+|$))|(?:^%transfiletriggerun(\s+|$))|(?:^%transfiletriggerpostun(\s+|$))',
        re.IGNORECASE,
    )
    re_spec_files = re.compile(r'^%files(\s+|$)', re.IGNORECASE)
    re_spec_changelog = re.compile(r'^%changelog\s*$', re.IGNORECASE)

    # rpmpreamble
    # WARNING: keep in sync with rpmcleaner Section change detection
    re_if = re.compile(
        r'^\s*(?:%{?if\s|%{?ifarch\s|%{?ifnarch\s|%{?if\S*}?(\s.*|)$)', re.IGNORECASE
    )
    re_codeblock = re.compile(
        r'^\s*((### COMMON-([a-zA-Z0-9]+)-BEGIN ###|# MANUAL BEGIN|# SECTION)(\s.*|)|# MANUAL)$',
        re.IGNORECASE,
    )
    re_else_elif = re.compile(r'^\s*%(else|elif)(\s.*|)$', re.IGNORECASE)
    re_endif = re.compile(r'^\s*%endif(\s.*|)$', re.IGNORECASE)
    re_endcodeblock = re.compile(
        r'^\s*(### COMMON-([a-zA-Z0-9]+)-END ###|# MANUAL END|# /MANUAL|# (END|/)SECTION)(\s.*|)$',
        re.IGNORECASE,
    )
    re_name = re.compile(r'^Name:\s*(\S*)', re.IGNORECASE)
    re_version = re.compile(r'^Version:\s*(.*)', re.IGNORECASE)
    re_release = re.compile(r'^Release:\s*(\S*)', re.IGNORECASE)
    re_license = re.compile(r'^License:\s*(.*)', re.IGNORECASE)
    re_summary = re.compile(r'^Summary:\s*(.*)', re.IGNORECASE)
    re_summary_localized = re.compile(r'^Summary(\(\S+\)):\s*(.*)', re.IGNORECASE)
    re_url = re.compile(r'^Url:\s*(\S*)', re.IGNORECASE)
    re_group = re.compile(r'^Group:\s*(.*)', re.IGNORECASE)
    re_vendor = re.compile(r'^Vendor:\s*(.*)', re.IGNORECASE)
    re_source = re.compile(r'^Source(\d*):\s*(.*)', re.IGNORECASE)
    re_nosource = re.compile(r'^NoSource:\s*(.*)', re.IGNORECASE)
    re_patch = re.compile(r'^((?:#[#\s]*)?)Patch(\d*):\s*(\S*)', re.IGNORECASE)
    re_buildrequires = re.compile(r'^(BuildRequires|BuildPreReq):\s*(.*)', re.IGNORECASE)
    re_buildconflicts = re.compile(r'^BuildConflicts:\s*(.*)', re.IGNORECASE)
    re_buildignores = re.compile(r'^#!BuildIgnore:\s*(.*)', re.IGNORECASE)
    re_prereq = re.compile(r'^PreReq:\s*(.*)', re.IGNORECASE)
    re_requires = re.compile(r'^Requires:\s*(.*)', re.IGNORECASE)
    re_requires_phase = re.compile(r'^Requires(\([^)]+\)):\s*(.*)', re.IGNORECASE)
    re_recommends = re.compile(r'^Recommends:\s*(.*)', re.IGNORECASE)
    re_suggests = re.compile(r'^Suggests:\s*(.*)', re.IGNORECASE)
    re_enhances = re.compile(r'^Enhances:\s*(.*)', re.IGNORECASE)
    re_supplements = re.compile(r'^Supplements:\s*(.*)', re.IGNORECASE)
    re_conflicts = re.compile(r'^Conflicts:\s*(.*)', re.IGNORECASE)
    re_provides = re.compile(r'^Provides:\s*(.*)', re.IGNORECASE)
    re_obsoletes = re.compile(r'^Obsoletes:\s*(.*)', re.IGNORECASE)
    re_removepath = re.compile(r'^\s*RemovePathPostfixes:\s*(.*)', re.IGNORECASE)
    re_buildroot = re.compile(r'^\s*BuildRoot:', re.IGNORECASE)
    re_buildarch = re.compile(r'^\s*BuildArch(itectures)?:\s*(.*)', re.IGNORECASE)
    re_exclusivearch = re.compile(r'^\s*ExclusiveArch(itectures)?:\s*(.*)', re.IGNORECASE)
    re_excludearch = re.compile(r'^\s*ExcludeArch(itectures)?:\s*(.*)', re.IGNORECASE)
    re_epoch = re.compile(r'^\s*Epoch:\s*(.*)', re.IGNORECASE)
    re_icon = re.compile(r'^\s*Icon:\s*(.*)', re.IGNORECASE)
    re_copyright = re.compile(r'^\s*Copyright:\s*(.*)', re.IGNORECASE)
    re_packager = re.compile(r'^\s*Packager:\s*(.*)', re.IGNORECASE)
    re_define = re.compile(r'^\s*%define\s*(.*)', re.IGNORECASE)
    re_global = re.compile(r'^\s*%global\s*(.*)', re.IGNORECASE)
    re_bcond_with = re.compile(r'^\s*%bcond_with(out)?\s*(.*)', re.IGNORECASE)
    re_autoreqprov = re.compile(r'^\s*AutoReqProv:.*$', re.IGNORECASE)
    re_debugpkg = re.compile(r'^%{?(debug_package|___debug_install_post)}?\s*$', re.IGNORECASE)
    re_py_requires = re.compile(r'^%{?\??py_requires}?\s*$', re.IGNORECASE)
    re_mingw = re.compile(r'^\s*%{?_mingw.*$', re.IGNORECASE)
    re_patterndefine = re.compile(r'^\s*%{?pattern_\S+}?\s*$', re.IGNORECASE)
    re_patternmacro = re.compile(r'pattern(-\S+)?\(\)', re.IGNORECASE)
    re_patternobsolete = re.compile(r'patterns-openSUSE-\S+', re.IGNORECASE)
    re_tail_macros = re.compile(r'^%{?python_subpackages}?')
    re_head_macros = re.compile(r'^%{?\??(sle15_python_module_pythons|sle15allpythons)}?')
    re_preamble_prefix = re.compile(r'^Prefix:\s*(.*)', re.IGNORECASE)
    # grab all macros with rpm call that query for version, this still might
    # be bit too greedy but it is good enough now
    re_rpm_command = re.compile(r'%\(\s*(rpm|echo\s+`rpm).*--queryformat\s+\'%{?VERSION}?\'.*\)')
    re_requires_eq = re.compile(r'^\s*(%{\?requires_eq:\s*)?%requires_eq\s*(.*)')
    re_requires_ge = re.compile(r'^\s*(%{\?requires_ge:\s*)?%requires_ge\s*(.*)')
    re_onelinecond = re.compile(r'^\s*%{!?[^?]*\?[^:]+:[^}]+}')
    # Special bracketed deps dection
    re_brackety_requires = re.compile(r'(pkgconfig|cmake|perl|tex|rubygem)\(')
    re_version_separator = re.compile(r'(\S+)((\s*[<>=\s]+)(\S+))*')
    # packageand(pkg1:pkg2)
    re_packageand = re.compile(r'^packageand\(\s*(\S+)\s*:\s*(\S+)\s*\)\s*$')
    # otherproviders(foo)
    re_otherproviders = re.compile(r'^otherproviders\(\s*(\S+)\s*\)\s*$')
    re_pypi_type = re.compile(r'^/packages/(?P<type>[\w|.]+)')
    re_pypi_modname = re.compile(r'^(?P<pkgname>[\w\.\_\-+]+|%{?\w+}?)\-(%{?\w+}?|[\d\.]+)')

    # rpmdescription
    re_authors = re.compile(r'^\s*Author(s)?:\s*')

    # rpmbuild
    re_jobs = re.compile(r'%{?(_smp_mflags|\?_smp_flags|\?jobs:\s*-j\s*%(jobs|{jobs}))}?')
    re_make = re.compile(r'(^\s*)make(\s.*|)$')
    re_make_build = re.compile(r'(^\s*)%make_build(\s.*|)$')
    re_optflags_quotes = re.compile(r'=\s*\${?RPM_OPT_FLAGS}?\s*$')
    re_optflags = re.compile(r'\${?RPM_OPT_FLAGS}?')
    re_suseupdateconfig = re.compile(r'%{?\??suse_update_config')
    re_configure = re.compile(r'(^|(.*\s)?)./configure(\s.*|)$')
    re_cmake = re.compile(r'(^|(.*\s)?)cmake(\s.*|)$')
    re_qmake5 = re.compile(r'(^|(.*\s)?)qmake-qt5(\s.*|)$')
    re_meson = re.compile(r'(^|(.*\s)?)meson(\s.*|)$')
    re_pytest = re.compile(
        r'%python_(expand|exec)\s+(PYTHONPATH=%{buildroot}%{\$?python_sitelib}\s+)?(\$?python\s+)?(%{_bindir}/?|-m\s+)?py\.?test(-(%{\$?python_version}|%{\$?python_bin_suffix})?)?(\s+(-v|-o addopts=-v))?'
    )
    re_pytest_arch = re.compile(
        r'%python_(expand|exec)\s+(PYTHONPATH=%{buildroot}%{\$?python_sitearch}\s+)?(\$?python\s+)?(%{_bindir}/?|-m\s+)?py\.?test(-(%{\$?python_version}|%{\$?python_bin_suffix})?)?(\s+(-v|-o addopts=-v))?'
    )
    re_pyunittest = re.compile(
        r'%python_(expand|exec)\s+(PYTHONPATH=%{buildroot}%{\$?python_sitelib}\s+)?(\$?python\s+)?-m\s+unittest(\s+discover)?'
    )
    re_pyunittest_arch = re.compile(
        r'%python_(expand|exec)\s+(PYTHONPATH=%{buildroot}%{\$?python_sitearch}\s+)?(\$?python\s+)?-m\s+unittest(\s+discover)?'
    )
    re_python_expand = re.compile(
        r'%{?(python_sitelib|python_sitearch|python_bin_suffix|python_version)}?'
    )
    re_python_interp_expand = re.compile(r'\s+(python)\s+')
    re_python_module = re.compile(r'.*\s%{python_module\s.*}')

    # rpmcopyright
    re_copyright_string = re.compile(r'^#\s*Copyright\ \(c\)\s*(.*)', re.IGNORECASE)
    re_suse_copyright = re.compile(
        r'SUSE (LLC\.?|LINUX (Products )?GmbH, Nuernberg, Germany\.)\s*$', re.IGNORECASE
    )
    re_rootforbuild = re.compile(r'^#\s*needsrootforbuild\s*$', re.IGNORECASE)
    re_binariesforbuild = re.compile(r'^#\s*needsbinariesforbuild\s*$', re.IGNORECASE)
    re_nodebuginfo = re.compile(r'^#\s*nodebuginfo\s*$', re.IGNORECASE)
    re_sslcerts = re.compile(r'^#\s*needssslcertforbuild\s*$', re.IGNORECASE)
    re_icecream = re.compile(r'^#\s*icecream\s*$', re.IGNORECASE)
    re_vimmodeline = re.compile(r'^#\s*vim:', re.IGNORECASE)
    re_skipcleaner = re.compile(r'^#\s*nospeccleaner\s*$', re.IGNORECASE)

    # rpminstall
    re_clean = re.compile(r'rm\s+(-?\w?\ ?)*"?(%{buildroot}|\$b)"?$')
    re_install = re.compile(
        r'{0}*(%{{makeinstall}}|make{0}+install){0}*$'.format(
            r'(DESTDIR=%{buildroot}|%{\?_smp_mflags}|\s|V=1|VERBOSE=1|-j\d+)'
        )
    )
    re_rm = re.compile(r'rm\s+(-?\w?\ ?)*"?(%{buildroot}|\$b)"?/?"?%{_lib(dir)?}.*\*\.la;?$')
    re_find = re.compile(
        r'find\s+"?(%{buildroot}|\$b)("?\S?/?)*\s*.*\s+-i?name\s+["\'\\]?\*\.la($|.*[^\\]$)'
    )
    re_find_double = re.compile(r'-i?name')
    re_rm_double = re.compile(r'(\.|{)a')

    # rpmprep
    re_patch_prep = re.compile(r'^%patch(\d+)\s*(.*)$')
    re_setup = re.compile(r'\s*-n\s+"?%{name}-%{version}"?($|\s)')
    re_dephell_setup = re.compile(r'\s*dephell[s]?.*convert')

    # rpmfiles
    re_man_compression = re.compile(r'(\d)(\.?\*|\.gz|%{?ext_man}?)$')
    re_info_compression = re.compile(r'\.info(\.?\*|\.gz|%{?ext_info}?)$')
    re_defattr = re.compile(r'^\s*%defattr\s*\(\s*-\s*,\s*root\s*,\s*root\s*(,\s*-\s*)?\)\s*')
    re_doclicense = re.compile(r'(\S+)?(LICEN(S|C)E|COPYING)(\*|\.(\*|\S+))?($|\s)', re.IGNORECASE)
    # python sitelib
    re_python_sitelib_glob = re.compile(r'^(?P<macro>%{(python\d*)_(sitelib|sitearch)})/\*$')
    re_python_package_name = re.compile(r'^python\d*-(.*)')

    # rpmscriptlets
    re_ldconfig = re.compile(r'(^|(.*\s)?)%{?run_ldconfig}?(\s.*|)$', re.IGNORECASE)
    # patches/sources
    re_ptch = re.compile(r'%{P:(\d+)}')
    re_src = re.compile(r'%{S:(\d+)}')

    # comment detection
    re_comment = re.compile(r'^$|^\s*#')

    # macro detection
    re_macro = re.compile(
        # find start of macro:
        #   either beggining of string or something which is not '%' or :
        #   where : is used after macro declaration we should not curlify
        r'(^|([^%:]))'
        +
        # macro itself:
        # '%' followed by either number not starting with '0'
        # or by chars where first is a-z or A-Z or underscore
        r'%([1-9]\d*|[a-zA-Z_]\w*'
        +
        # possibly followed by parens
        r'(\s*\([^)]*\))?'
        +
        # beyond the end of the macro
        r')(|(\W))'
    )

    # cleaning path regexps
    endmacro = r'([/\s%"]|$)'
    re_oldprefix = re.compile(r'%{?_exec_prefix}?' + endmacro)
    re_prefix = re.compile(r'(?<!\w)/usr' + endmacro)
    re_bindir = re.compile(r'%{?_prefix}?/bin' + endmacro)
    re_sbindir = re.compile(r'%{?_prefix}?/sbin' + endmacro)
    re_libexecdir = re.compile(r'%{?_prefix}?/libexec' + endmacro)
    re_includedir = re.compile(r'%{?_prefix}?/include' + endmacro)
    re_datadir = re.compile(r'%{?_prefix}?/share' + endmacro)
    re_mandir = re.compile(r'%{?_datadir}?/man' + endmacro)
    re_infodir = re.compile(r'%{?_datadir}?/info' + endmacro)
    re_docdir = re.compile(r'%{?_datadir}?/doc/packages' + endmacro)
    re_initdir = re.compile(r'/etc/init.d' + endmacro)
    re_sysconfdir = re.compile(r'/etc' + endmacro)
    re_localstatedir = re.compile(r'/var' + endmacro)
    re_libdir = re.compile(r'%{?_prefix}?/(%{?_lib}?|lib64)' + endmacro)
    re_initddir = re.compile(r'%{?_initrddir}?' + endmacro)
    re_rpmbuildroot = re.compile(r'(\${?RPM_BUILD_ROOT}?|"%{?buildroot}?")([/\s%]|$)')
    re_rpmbuildroot_quotes = re.compile(r'"\${?RPM_BUILD_ROOT}?"')
    # deprecated greps
    re_deprecated_egrep_regex = re.compile(r'\begrep\b')
    re_deprecated_fgrep_regex = re.compile(r'\bfgrep\b')

    def __init__(self, keywords: List[str]) -> None:
        """Compile all the keywords that are to be unbraced."""
        self.re_unbrace_keywords = re.compile('%{(' + '|'.join(keywords) + ')}')
