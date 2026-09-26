import pytest

from spec_cleaner import RpmSpecCleaner
from spec_cleaner.rpmsection import Section


def _default_options(tmp_path):
    """Create the default options dict for tests."""
    specfile = tmp_path / 'test.spec'
    specfile.write_text('Name: test\n')
    return {
        'specfile': str(specfile),
        'output': str(tmp_path / 'out.spec'),
        'pkgconfig': False,
        'inline': False,
        'diff': False,
        'diff_prog': 'vimdiff',
        'minimal': False,
        'no_curlification': False,
        'suse_copyright': False,
        'copyright_year': 2013,
        'remove_groups': False,
        'tex': False,
        'perl': False,
        'cmake': False,
        'keep_space': False,
    }


def _section(tmp_path, defined_macros):
    options = RpmSpecCleaner(_default_options(tmp_path)).options
    options['defined_macros'] = defined_macros
    return Section(options)


# The trigger line is spelled in the form only this rule can match, otherwise an earlier
# rule rewrites it and the guard of this rule becomes unobservable.
KNOWN_DIR_RULES = [
    ('echo %_exec_prefix', 'echo %{_prefix}', ('_exec_prefix', '_prefix')),
    ('echo /usr', 'echo %{_prefix}', ('_prefix',)),
    ('echo %{_prefix}/bin', 'echo %{_bindir}', ('_prefix', '_exec_prefix', '_bindir')),
    ('echo %{_prefix}/sbin', 'echo %{_sbindir}', ('_prefix', '_exec_prefix', '_sbindir')),
    (
        'echo %{_prefix}/libexec',
        'echo %{_libexecdir}',
        ('_prefix', '_exec_prefix', '_libexecdir'),
    ),
    ('echo %{_prefix}/include', 'echo %{_includedir}', ('_prefix', '_includedir')),
    ('echo %{_prefix}/share', 'echo %{_datadir}', ('_prefix', '_datarootdir', '_datadir')),
    ('echo %{_datadir}/man', 'echo %{_mandir}', ('_datadir', '_mandir')),
    ('echo %{_datadir}/info', 'echo %{_infodir}', ('_datadir', '_infodir')),
    ('echo %{_datadir}/doc/packages', 'echo %{_docdir}', ('_datadir', '_docdir')),
    ('echo /etc/init.d', 'echo %{_initddir}', ('_sysconfdir', '_initddir')),
    ('echo /etc', 'echo %{_sysconfdir}', ('_sysconfdir',)),
    ('echo /var', 'echo %{_localstatedir}', ('_localstatedir',)),
    (
        'echo %{_prefix}/lib64/ocaml',
        'echo %{ocaml_standard_library}',
        ('_prefix', 'ocaml_standard_library'),
    ),
    ('echo %{_prefix}/lib64', 'echo %{_libdir}', ('_prefix', '_exec_prefix', '_lib', '_libdir')),
    (
        'echo %{_prefix}/lib/systemd/system',
        'echo %{_unitdir}',
        ('_prefix', '_unitdir'),
    ),
    ('echo %{_prefix}/lib/tmpfiles.d', 'echo %{_tmpfilesdir}', ('_prefix', '_tmpfilesdir')),
    ('echo %{_prefix}/lib/sysusers.d', 'echo %{_sysusersdir}', ('_prefix', '_sysusersdir')),
    (
        'echo %{_prefix}/lib/udev/rules.d',
        'echo %{_udevrulesdir}',
        ('_prefix', '_udevrulesdir'),
    ),
    ('echo %{_prefix}/lib/sysctl.d', 'echo %{_sysctldir}', ('_prefix', '_sysctldir')),
    (
        'echo %{_prefix}/lib/perl5/vendor_perl/%{perl_version}',
        'echo %{perl_vendorlib}',
        ('_prefix', 'perl_version', 'perl_vendorlib'),
    ),
    ('echo %{_datadir}/fonts', 'echo %{_fontsdir}', ('_datadir', '_fontsdir')),
    (
        'echo %{_datadir}/emacs/site-lisp',
        'echo %{_emacs_sitelispdir}',
        ('_datadir', '_emacs_sitelispdir'),
    ),
    (
        'echo %{_sysconfdir}/apparmor.d',
        'echo %{apparmor_profilesdir}',
        ('_sysconfdir', 'apparmor_profilesdir'),
    ),
    (
        'echo %{_prefix}/lib/node_modules',
        'echo %{nodejs_sitelib}',
        ('_prefix', 'nodejs_sitelib'),
    ),
    ('echo %_initrddir', 'echo %{_initddir}', ('_initrddir', '_initddir')),
]

KNOWN_DIR_MACROS = sorted({macro for _, _, macros in KNOWN_DIR_RULES for macro in macros})


@pytest.mark.parametrize(('line', 'expected', 'macros'), KNOWN_DIR_RULES)
def test_rewrite_with_default_macros(tmp_path, line, expected, macros):
    """Each rule rewrites its own line while none of the macros it reads is redefined."""
    assert _section(tmp_path, set()).replace_known_dirs(line) == expected


@pytest.mark.parametrize(('line', 'expected', 'macros'), KNOWN_DIR_RULES)
def test_rewrite_disabled_by_redefined_macro(tmp_path, line, expected, macros):
    """Redefining any of the macros a rule reads switches that rule off."""
    # A neighbouring rule may still rewrite the line, so assert on the target replacement
    # being absent rather than on the line staying untouched.
    for macro in macros:
        assert expected not in _section(tmp_path, {macro}).replace_known_dirs(line)


def test_every_guard_macro_is_covered():
    """Every macro name in the rules table is exercised as a redefinition."""
    assert len(KNOWN_DIR_MACROS) == 29
