import time
from collections.abc import Callable
from typing import Any

import pytest

from spec_cleaner.rpmcheck import RpmCheck
from spec_cleaner.rpmcleaner import RpmSpecCleaner
from spec_cleaner.rpmregexp import Regexp
from spec_cleaner.rpmsection import Section


def _section(default_options: Callable[..., dict[str, Any]], defined_macros: set[str]) -> Section:
    options = RpmSpecCleaner(default_options()).options
    options['defined_macros'] = defined_macros
    return Section(options)


# The trigger line is spelled in the form only this rule can match, otherwise an earlier
# rule rewrites it and the guard of this rule becomes unobservable.
KNOWN_DIR_RULES: list[tuple[str, str, tuple[str, ...]]] = [
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
def test_rewrite_with_default_macros(
    default_options: Callable[..., dict[str, Any]],
    line: str,
    expected: str,
    macros: tuple[str, ...],
) -> None:
    """Each rule rewrites its own line while none of the macros it reads is redefined."""
    assert _section(default_options, set()).replace_known_dirs(line) == expected


@pytest.mark.parametrize(('line', 'expected', 'macros'), KNOWN_DIR_RULES)
def test_rewrite_disabled_by_redefined_macro(
    default_options: Callable[..., dict[str, Any]],
    line: str,
    expected: str,
    macros: tuple[str, ...],
) -> None:
    """Redefining any of the macros a rule reads switches that rule off."""
    # A neighbouring rule may still rewrite the line, so assert on the target replacement
    # being absent rather than on the line staying untouched.
    for macro in macros:
        assert expected not in _section(default_options, {macro}).replace_known_dirs(line)


def test_every_guard_macro_is_covered() -> None:
    """Every macro name in the rules table is exercised as a redefinition."""
    assert len(KNOWN_DIR_MACROS) == 28


def test_fontsdir_is_not_a_rewrite_target(
    default_options: Callable[..., dict[str, Any]],
) -> None:
    """%{_fontsdir} needs fontpackages-devel, so a fonts path macroises only to %{_datadir} (gh#528)."""
    section = _section(default_options, set())
    assert section.replace_known_dirs('echo /usr/share/fonts') == 'echo %{_datadir}/fonts'
    assert section.replace_known_dirs('echo %{_datadir}/fonts') == 'echo %{_datadir}/fonts'
    assert '%{_fontsdir}' not in section.replace_known_dirs(
        'install -D foo %{buildroot}/usr/share/fonts/foo.ttf'
    )


def _check(default_options: Callable[..., dict[str, Any]]) -> RpmCheck:
    options = RpmSpecCleaner(default_options()).options
    options['defined_macros'] = set()
    return RpmCheck(options)


def test_replace_make_stops_flag_cleanup_at_command_boundary(
    default_options: Callable[..., dict[str, Any]],
) -> None:
    """Test that flag cleanup stops at the next shell command boundary."""
    replace_make = _check(default_options)._replace_make
    # an assignment belonging to a later command survives verbatim
    assert (
        replace_make('cd tests && make check; V=1 ./verify')
        == 'cd tests && %make_build check; V=1 ./verify'
    )
    assert (
        replace_make('make check %{?_smp_mflags}; V=1 ./verify')
        == '%make_build check; V=1 ./verify'
    )
    assert (
        replace_make('cd tests && make check && V=1 ./verify')
        == 'cd tests && %make_build check && V=1 ./verify'
    )
    assert replace_make('make check; VERBOSE=1 ./verify') == '%make_build check; VERBOSE=1 ./verify'
    # flags of the make call itself are still stripped
    assert replace_make('make check V=1') == '%make_build check'
    assert replace_make('make check %{?_smp_mflags}') == '%make_build check'
    # a separator inside quotes is not a boundary
    assert replace_make('make check FOO="a;b" V=1') == '%make_build check FOO="a;b"'
    # a make inside quotes is never rewritten, even when the line has
    # a real separator later on
    assert replace_make('echo "a; make all"') == 'echo "a; make all"'
    assert replace_make('echo "a; make all"; make check') == 'echo "a; make all"; %make_build check'


def _cleaned_line(default_options: Callable[..., dict[str, Any]], minimal: bool, line: str) -> str:
    options = RpmSpecCleaner(default_options(minimal=minimal)).options
    options['defined_macros'] = set()
    section = Section(options)
    section.add(line)
    return section.lines[0]


MACRO_FORM_REWRITES = [
    ('cp %{S:1} .', 'cp %{SOURCE1} .'),
    ('cp %{S:0} %{P:0} .', 'cp %{SOURCE0} %{PATCH0} .'),
    ('cp %{S:1} %{S:2} %{P:12} .', 'cp %{SOURCE1} %{SOURCE2} %{PATCH12} .'),
    ('tar xf prefix-%{S:1}.tar.xz', 'tar xf prefix-%{SOURCE1}.tar.xz'),
    ('echo %{?with_extra:%{S:2}}', 'echo %{?with_extra:%{SOURCE2}}'),
]

# Spellings outside the rewritten family: the already-long form, a
# non-numeric suffix and comment lines pass the cleanup unchanged.
MACRO_FORM_UNTOUCHED = [
    'cp %{SOURCE1} .',
    'echo %{S:foo}',
    '# comment mentioning %{S:1}',
]


@pytest.mark.parametrize(('line', 'expected'), MACRO_FORM_REWRITES)
def test_macro_form_rewritten_in_full_mode(
    default_options: Callable[..., dict[str, Any]], line: str, expected: str
) -> None:
    """The full run spells short source/patch forms out to the long form."""
    assert _cleaned_line(default_options, False, line) == expected


@pytest.mark.parametrize(('line', 'expected'), MACRO_FORM_REWRITES)
def test_macro_form_kept_in_minimal_mode(
    default_options: Callable[..., dict[str, Any]], line: str, expected: str
) -> None:
    """The minimal run keeps the source/patch spelling as written."""
    assert _cleaned_line(default_options, True, line) == line


@pytest.mark.parametrize('line', MACRO_FORM_UNTOUCHED)
def test_macro_form_neighbours_untouched(
    default_options: Callable[..., dict[str, Any]], line: str
) -> None:
    """Forms outside the family stay untouched in both modes."""
    for minimal in (False, True):
        assert _cleaned_line(default_options, minimal, line) == line


def test_unbraced_source_form_kept_in_minimal_mode(
    default_options: Callable[..., dict[str, Any]],
) -> None:
    """The unbraced long form is not part of the family and stays as written."""
    assert _cleaned_line(default_options, True, 'cp %SOURCE2 .') == 'cp %SOURCE2 .'


def test_version_guard_rewrite_runs_in_both_modes(
    default_options: Callable[..., dict[str, Any]],
) -> None:
    """The %{suse_version} guard insertion changes expansion, so it is no respelling and keeps firing."""
    for minimal in (False, True):
        assert (
            _cleaned_line(default_options, minimal, 'echo %{suse_version}')
            == 'echo 0%{?suse_version}'
        )


def test_known_dirs_replaced_in_full_run(default_options: Callable[..., dict[str, Any]]) -> None:
    """The full run rewrites a literal path to its directory macro."""
    line = 'install -D -m 0755 foo /usr/bin/foo'
    assert _cleaned_line(default_options, False, line) == 'install -D -m 0755 foo %{_bindir}/foo'


def test_known_dirs_kept_in_minimal_run(default_options: Callable[..., dict[str, Any]]) -> None:
    """The minimal run keeps literal paths as written."""
    line = 'install -D -m 0755 foo /usr/bin/foo'
    assert _cleaned_line(default_options, True, line) == line


# gh#519: a path-valued BuildRequires must stay literal in the full run.
# The OBS scheduler records BuildRequires unexpanded, so a macroised file
# dependency matches nothing and the build goes unresolvable.
PATH_BUILDREQUIRES_KEPT = [
    'BuildRequires:  /usr/bin/zcat',
    'BuildRequires:  /usr/bin/gpg',
    'BuildRequires:  /usr/bin/make',
    'BuildRequires:  /usr/sbin/foo',
    'BuildRequires:  foo /usr/bin/make',
    # a path right after '(' in a rich dependency
    'BuildRequires:  (/usr/bin/foo or bar)',
    'BuildRequires:  (foo or /usr/bin/bar)',
    # the tag inside a one-line conditional is still a BuildRequires
    '%{?with_foo:BuildRequires: /usr/bin/foo}',
    # the tag inside a one-line conditional may be a dep pragma
    '%{?with_foo:#!BuildRequires: /usr/bin/foo}',
    '%{!?with_foo:#!BuildRequires: /usr/bin/foo}',
]


@pytest.mark.parametrize('line', PATH_BUILDREQUIRES_KEPT)
def test_path_buildrequires_kept_in_full_run(
    default_options: Callable[..., dict[str, Any]], line: str
) -> None:
    """A file BuildRequires stays literal in the full run (gh#519)."""
    assert _cleaned_line(default_options, False, line) == line


def test_requires_path_still_macroised_in_full_run(
    default_options: Callable[..., dict[str, Any]],
) -> None:
    """The carve-out is BuildRequires-only; a path in Requires still macroises."""
    assert (
        _cleaned_line(default_options, False, 'Requires:  /usr/bin/foo')
        == 'Requires:  %{_bindir}/foo'
    )


def test_conditional_requires_path_still_macroised_in_full_run(
    default_options: Callable[..., dict[str, Any]],
) -> None:
    """A path in a conditional Requires still macroises; only BuildRequires is exempt."""
    assert (
        _cleaned_line(default_options, False, '%{?with_foo:Requires: /usr/bin/foo}')
        == '%{?with_foo:Requires: %{_bindir}/foo}'
    )


def test_conditional_pragma_requires_path_still_macroised_in_full_run(
    default_options: Callable[..., dict[str, Any]],
) -> None:
    """A path in a conditional pragma Requires still macroises; only BuildRequires is exempt."""
    assert (
        _cleaned_line(default_options, False, '%{?with_foo:#!Requires: /usr/bin/foo}')
        == '%{?with_foo:#!Requires: %{_bindir}/foo}'
    )


def test_buildrequires_comment_slash_does_not_exempt(
    default_options: Callable[..., dict[str, Any]],
) -> None:
    """A `/` in a trailing comment is not a path dependency (gh#519)."""
    assert (
        _cleaned_line(default_options, False, 'BuildRequires:  foo # needs /usr/bin/foo')
        == 'BuildRequires:  foo # needs %{_bindir}/foo'
    )


def test_path_buildrequires_comment_still_macroised(
    default_options: Callable[..., dict[str, Any]],
) -> None:
    """A path in a trailing comment macroises even when the value is a path (gh#519)."""
    assert (
        _cleaned_line(
            default_options,
            False,
            'BuildRequires:  /usr/bin/foo # see /usr/bin/bar for details',
        )
        == 'BuildRequires:  /usr/bin/foo # see %{_bindir}/bar for details'
    )


def test_path_buildrequires_dnl_comment_still_macroised(
    default_options: Callable[..., dict[str, Any]],
) -> None:
    """A path in a %dnl comment macroises even when the value is a path (gh#519)."""
    assert (
        _cleaned_line(default_options, False, 'BuildRequires:  /usr/bin/foo %dnl /usr/bin/bar')
        == 'BuildRequires:  /usr/bin/foo %dnl %{_bindir}/bar'
    )


def test_path_buildrequires_comment_separator_kept(
    default_options: Callable[..., dict[str, Any]],
) -> None:
    """The whitespace before a trailing comment is kept verbatim (gh#519)."""
    assert (
        _cleaned_line(
            default_options,
            False,
            'BuildRequires:  /usr/bin/foo  # see /usr/bin/bar',
        )
        == 'BuildRequires:  /usr/bin/foo  # see %{_bindir}/bar'
    )


def test_dnl_inside_macro_body_is_not_a_comment(
    default_options: Callable[..., dict[str, Any]],
) -> None:
    """A `%dnl` inside a macro body is body text; the next one starts the comment (gh#519)."""
    assert (
        _cleaned_line(
            default_options,
            False,
            'BuildRequires:  foo %{foo %dnl} bar %dnl /usr/bin/baz',
        )
        == 'BuildRequires:  foo %{foo %dnl} bar %dnl %{_bindir}/baz'
    )


def test_path_before_dnl_inside_macro_body_stays_literal(
    default_options: Callable[..., dict[str, Any]],
) -> None:
    """A `%dnl` inside a macro body does not hide the path before it (gh#519)."""
    assert (
        _cleaned_line(
            default_options,
            False,
            'BuildRequires:  /usr/bin/foo %{foo %dnl} bar %dnl comment',
        )
        == 'BuildRequires:  /usr/bin/foo %{foo %dnl} bar %dnl comment'
    )


def test_buildroot_replaced_in_minimal_run(default_options: Callable[..., dict[str, Any]]) -> None:
    """$RPM_BUILD_ROOT is a variable substitution and is replaced in both modes."""
    line = 'install -D -m 0644 foo.conf $RPM_BUILD_ROOT/usr/share/foo/foo.conf'
    expected = 'install -D -m 0644 foo.conf %{buildroot}/usr/share/foo/foo.conf'
    assert _cleaned_line(default_options, True, line) == expected


# gh#491: curlification is only safe for a bare macro reference. A name
# carrying an argument list is an invocation, a name directly followed
# by '(' may also just carry a literal parenthesised suffix, and the
# %-forms inside a lua body are program text.
EMBRACE_INVOCATION_REWRITES = [
    # only the bare references around the invocation are braced
    (
        'Provides: %name(xfrm6_raw) = %version-%release',
        'Provides: %name(xfrm6_raw) = %{version}-%{release}',
    ),
    # a bare name is still braced, also in front of parenthesised text
    ('Summary: test %name (a library)', 'Summary: test %{name} (a library)'),
    ('echo %version (release %release)', 'echo %{version} (release %{release})'),
]

EMBRACE_INVOCATION_UNTOUCHED = [
    # an invocation with a parenthesised argument list
    '%lang_package(cryptsetup)',
    'Provides: %plainpython(abi) = 3',
    # the already braced invocation form is left alone as well
    '%{lang_package(cryptsetup)}',
]


@pytest.mark.parametrize(('line', 'expected'), EMBRACE_INVOCATION_REWRITES)
def test_embrace_keeps_invocations_and_braces_bare_names(
    default_options: Callable[..., dict[str, Any]], line: str, expected: str
) -> None:
    """Invocations keep their form while bare references around them are braced."""
    assert _cleaned_line(default_options, False, line) == expected


@pytest.mark.parametrize('line', EMBRACE_INVOCATION_UNTOUCHED)
def test_embrace_leaves_invocations_untouched(
    default_options: Callable[..., dict[str, Any]], line: str
) -> None:
    """A macro invocation with an argument list is not braced as a plain reference."""
    assert _cleaned_line(default_options, False, line) == line


# gh#321: macros inside a python_module invocation are its arguments,
# so they are not braced even when the invocation starts the line.
@pytest.mark.parametrize(
    'line',
    [
        '%{python_module %name}',
        '%{?python_module %name}',
        '%python_module %name',
        '%{prefixed_python_module %name}',
    ],
)
def test_python_module_line_start_not_embraced(
    default_options: Callable[..., dict[str, Any]], line: str
) -> None:
    """A python_module invocation at the start of the line keeps its macros unbraced."""
    assert _cleaned_line(default_options, False, line) == line


EMBRACE_VALUE_POSITIONS = [
    # a braced use of an argument-taking macro keeps its braces where
    # the following tokens belong to the surrounding grammar: unbraced,
    # rpm would hand them to the macro as its arguments (gh#500)
    ('Requires: %{typelib} = %{version}', 'Requires: %{typelib} = %{version}'),
    ('%files %{python_files} -f python-test.lang', '%files %{python_files} -f python-test.lang'),
    (
        'Summary: Haskell %{pkg_name} library documentation',
        'Summary: Haskell %{pkg_name} library documentation',
    ),
    # glued to a word character the suffix would merge into the macro
    # name of the unbraced form, so the use keeps its braces
    ('Requires: %{typelib}foo', 'Requires: %{typelib}foo'),
    # glued to a delimiter the use takes no arguments and still unbraces
    ('Name: ghc-%{pkg_name}', 'Name: ghc-%pkg_name'),
    # closing the line the use takes no arguments and still unbraces
    ('%package -n %{typelib}', '%package -n %typelib'),
    # an invocation in the space form keeps its form
    ('%python_module devel', '%python_module devel'),
]


@pytest.mark.parametrize(('line', 'expected'), EMBRACE_VALUE_POSITIONS)
def test_embrace_value_positions(
    default_options: Callable[..., dict[str, Any]], line: str, expected: str
) -> None:
    """Braced uses in value positions keep their braces, the rest of the unbracing stays."""
    assert _cleaned_line(default_options, False, line) == expected


EMBRACE_COMMAND_POSITIONS = [
    # rpm passes no arguments to a braced use in command position
    # either: the tokens behind it stay on the command line the macro
    # expands to, while unbraced they would go to the macro's option
    # parser ('Unknown option - in cargo_build()')
    ('%{cargo_build} --locked -p foo', '%{cargo_build} --locked -p foo'),
    ('%{cargo_test} -p foo', '%{cargo_test} -p foo'),
    ('%{ldconfig_scriptlets} -n foo', '%{ldconfig_scriptlets} -n foo'),
    # the same holds in the body of a conditional macro
    ('%{?with_check:%{cargo_test} -p foo}', '%{?with_check:%{cargo_test} -p foo}'),
    # closing the line the use takes no arguments and still unbraces
    ('%{cargo_build}', '%cargo_build'),
]


@pytest.mark.parametrize(('line', 'expected'), EMBRACE_COMMAND_POSITIONS)
def test_embrace_command_positions(
    default_options: Callable[..., dict[str, Any]], line: str, expected: str
) -> None:
    """Braced uses in command position keep their braces when tokens follow them."""
    assert _cleaned_line(default_options, False, line) == expected


EMBRACE_GLUED_KEYWORDS = [
    # a braced use of a plain keyword glued to a word character keeps
    # its braces: the unbraced form would merge the suffix into the
    # macro name, so rpm would read a different macro
    ('Requires: %{patch0}foo', 'Requires: %{patch0}foo'),
    ('echo %{setup}2', 'echo %{setup}2'),
    ('Summary: %{ghost}foo files', 'Summary: %{ghost}foo files'),
    # glued to a delimiter the use still unbraces
    ('echo %{patch0}-p1', 'echo %patch0-p1'),
    ('%{ghost}/run/foo', '%ghost/run/foo'),
    # closing the line the use still unbraces
    ('echo %{ghost}', 'echo %ghost'),
]


@pytest.mark.parametrize(('line', 'expected'), EMBRACE_GLUED_KEYWORDS)
def test_embrace_glued_keywords(
    default_options: Callable[..., dict[str, Any]], line: str, expected: str
) -> None:
    """Braced uses of plain keywords glued to a word character keep their braces."""
    assert _cleaned_line(default_options, False, line) == expected


# gh#522: a find/stat -printf/-fprintf/--printf format string carries
# %-directives that belong to the tool, not to rpm. The brace-the-macros
# pass must leave them alone, or the build fails when GNU find rejects
# the braced form (%{ is reserved for future use). Only the format
# string is shielded, so a bare macro elsewhere on the line is braced.
EMBRACE_PRINTF_FORMATS = [
    # the util-linux case: %f is find's basename directive
    (
        '  -printf "%{_mandir}/man8/%f*\\n" >> %{name}.files',
        '  -printf "%{_mandir}/man8/%f*\\n" >> %{name}.files',
    ),
    (
        '  -printf "%{_bindir}/%f\\n" >> %{name}.files',
        '  -printf "%{_bindir}/%f\\n" >> %{name}.files',
    ),
    # single-quoted formats and other directives
    (
        'find . -xtype l -delete -printf "deleted \'%f\'\\n"',
        'find . -xtype l -delete -printf "deleted \'%f\'\\n"',
    ),
    ("find . -printf '%p#\\n'", "find . -printf '%p#\\n'"),
    ('find * -name \\*.so -printf "/%p\\n"', 'find * -name \\*.so -printf "/%p\\n"'),
    ("find $root -name FEATURE -printf ' -I%h'", "find $root -name FEATURE -printf ' -I%h'"),
    ("find -type l -printf '%f\\a%l\\n'", "find -type l -printf '%f\\a%l\\n'"),
    # -fprintf takes a file argument before the format string
    (
        'find . -type f -fprintf /tmp/out.txt "%p %s\\n"',
        'find . -type f -fprintf /tmp/out.txt "%p %s\\n"',
    ),
    # unquoted formats: the format runs to the next shell separator,
    # and a bare macro elsewhere on the line is still braced
    ('find . -type f -printf %p\\n', 'find . -type f -printf %p\\n'),
    ('find . -type f -fprintf f %p\\n', 'find . -type f -fprintf f %p\\n'),
    (
        'find . -type f -printf %p -o -type d -printf %d\\n',
        'find . -type f -printf %p -o -type d -printf %d\\n',
    ),
    (
        'find /usr/share/foo -type f -printf %p\\n >> %{name}.files',
        'find %{_datadir}/foo -type f -printf %p\\n >> %{name}.files',
    ),
    # stat --printf takes its format after = or a space; the format may
    # also be unquoted (--printf=%a), and the path is still macroised
    (
        'test 1777 = "$(stat --printf=\'%a\' /var/spool/mail/)" || exit 1',
        'test 1777 = "$(stat --printf=\'%a\' %{_localstatedir}/spool/mail/)" || exit 1',
    ),
    (
        "stat --printf '%a' /var/spool/mail/",
        "stat --printf '%a' %{_localstatedir}/spool/mail/",
    ),
    (
        'stat --printf=%a /var/spool/mail/',
        'stat --printf=%a %{_localstatedir}/spool/mail/',
    ),
    # a bare macro outside the format string is still braced
    (
        'install -D -m 0644 foo.conf %buildroot/usr/share/foo/foo.conf',
        'install -D -m 0644 foo.conf %{buildroot}%{_datadir}/foo/foo.conf',
    ),
    # a braced macro inside the format string stays verbatim: the format
    # shield runs before the braced-argument-macro shield, so the two
    # shields never nest and no placeholder is left behind
    (
        '-printf "%{cargo_build} %f\\n" >> %{name}.files',
        '-printf "%{cargo_build} %f\\n" >> %{name}.files',
    ),
]


@pytest.mark.parametrize(('line', 'expected'), EMBRACE_PRINTF_FORMATS)
def test_embrace_leaves_printf_format_directives(
    default_options: Callable[..., dict[str, Any]], line: str, expected: str
) -> None:
    """%-directives in a -printf/--printf format string stay unbraced."""
    assert _cleaned_line(default_options, False, line) == expected


# gh#522: the same brace-the-macros pass also rewrote the %-directives of
# other tools' format strings. printf/sprintf (shell builtin,
# /usr/bin/printf, perl/ruby, awk) and awk's printf/sprintf inside the
# program carry %-directives that belong to the tool, not to rpm.
EMBRACE_SHELL_PRINTF_FORMATS = [
    # shell builtin / /usr/bin/printf, double- and single-quoted
    (
        'printf "%s\\n%s" "$MIN_TIME_VERSION" "$MIN_PG_VERSION"',
        'printf "%s\\n%s" "$MIN_TIME_VERSION" "$MIN_PG_VERSION"',
    ),
    ('printf "%d%02d" $maj $min', 'printf "%d%02d" $maj $min'),
    ('printf \'%s\' "6-zig-..."', 'printf \'%s\' "6-zig-..."'),
    (
        "printf 'Name: Proton Core\\nVersion: %{version}\\n'",
        "printf 'Name: Proton Core\\nVersion: %{version}\\n'",
    ),
    # perl/ruby paren form, and printf's -- and -v options
    ('return printf("%d.%d.%d\\n",', 'return printf("%d.%d.%d\\n",'),
    ('printf -- "%s\\n" foo', 'printf -- "%s\\n" foo'),
    ('printf -v var "%s\\n"', 'printf -v var "%s\\n"'),
    ('sprintf "%s" $x', 'sprintf "%s" $x'),
    # awk printf/sprintf inside the program
    (
        'awk -F. \'{ printf "%d.%03d%03d", $1, $2, $3 }\'',
        'awk -F. \'{ printf "%d.%03d%03d", $1, $2, $3 }\'',
    ),
    # a + inside the printf format must not be fragmented by the date
    # shield: the whole quoted string is shielded as one unit
    ('printf "%+d" $x', 'printf "%+d" $x'),
    # a bare macro outside the format string is still braced
    (
        'printf "%s\\n" /usr/share/foo',
        'printf "%s\\n" %{_datadir}/foo',
    ),
    # a '#' inside the format is not a comment
    ('printf "%s # x\\n" %name', 'printf "%s # x\\n" %{name}'),
    # a real comment is still left alone
    ('make %name # %foo', 'make %{name} # %foo'),
    # a date format nested in a printf format leaves no placeholder behind
    (
        'printf "Date: $(date "+%F") %name\\n"',
        'printf "Date: $(date "+%F") %name\\n"',
    ),
]


@pytest.mark.parametrize(('line', 'expected'), EMBRACE_SHELL_PRINTF_FORMATS)
def test_embrace_leaves_shell_printf_format_directives(
    default_options: Callable[..., dict[str, Any]], line: str, expected: str
) -> None:
    """%-directives in a printf/sprintf format string stay unbraced."""
    assert _cleaned_line(default_options, False, line) == expected


# gh#522: date(1) '+FORMAT' carries strftime %-directives (%Y, %m, %d,
# %s, ...) that belong to date, not to rpm. The + sits either outside
# the quotes ('+%s', '+ "%s"') or inside them ('"+%s"', ''+%Y%m%d'').
EMBRACE_DATE_FORMATS = [
    # + outside the quotes, format unquoted
    ('date +%Y-%m-%d', 'date +%Y-%m-%d'),
    ('date -r LICENSE +%s', 'date -r LICENSE +%s'),
    ('date -u +%Y-%m-%dT%H:%M:%SZ', 'date -u +%Y-%m-%dT%H:%M:%SZ'),
    # + inside the quotes
    ('date "+%s"', 'date "+%s"'),
    ('date -u -d "..." "+%s"', 'date -u -d "..." "+%s"'),
    ("date '+%Y%m%d'", "date '+%Y%m%d'"),
    ("date -u '+%FT%T%z'", "date -u '+%FT%T%z'"),
    ('date --date="$..." \'+%%F %T%z\'', 'date --date="$..." \'+%%F %T%z\''),
    # + outside the quotes, format quoted
    (
        'date -r %{SOURCE1} "+%B %d, %Y"',
        'date -r %{SOURCE1} "+%B %d, %Y"',
    ),
    ("date --date=@... +'\\\\date{%B %Y}'", "date --date=@... +'\\\\date{%B %Y}'"),
    # a bare macro outside the format string is still braced
    (
        'date +%Y-%m-%d /usr/share/foo',
        'date +%Y-%m-%d %{_datadir}/foo',
    ),
    # the S: macro rewrite still applies outside the format string
    ('date +%s -r %{S:99}', 'date +%s -r %{SOURCE99}'),
]


@pytest.mark.parametrize(('line', 'expected'), EMBRACE_DATE_FORMATS)
def test_embrace_leaves_date_format_directives(
    default_options: Callable[..., dict[str, Any]], line: str, expected: str
) -> None:
    """Strftime %-directives in a date '+FORMAT' argument stay unbraced."""
    assert _cleaned_line(default_options, False, line) == expected


def test_date_format_shield_is_linear(default_options: Callable[..., dict[str, Any]]) -> None:
    """An escaped quote opens no date format, so a long run of them stays fast."""
    section = _section(default_options, set())
    start = time.perf_counter()
    section.embrace_macros('date %name ' + '"+\\' * 20000)
    assert time.perf_counter() - start < 1


# gh#522: stat(1) -c/--format carries %-directives (%n, %s, %a, %Y, ...)
# that belong to stat, not to rpm. (stat --printf is covered by
# EMBRACE_PRINTF_FORMATS above.)
EMBRACE_STAT_FORMATS = [
    ("stat -c '%G' /usr/bin/foo", "stat -c '%G' %{_bindir}/foo"),
    ('stat -c "%a" /usr/bin/foo', 'stat -c "%a" %{_bindir}/foo'),
    ('stat -c %Y /usr/bin/foo', 'stat -c %Y %{_bindir}/foo'),
    # the format may be attached to the short -c with no separator
    ('stat -c%a /usr/bin/foo', 'stat -c%a %{_bindir}/foo'),
    ('stat --format="%y" /usr/bin/foo', 'stat --format="%y" %{_bindir}/foo'),
    ('stat -c %U:%G:%a /usr/bin/foo', 'stat -c %U:%G:%a %{_bindir}/foo'),
    ('stat -L -c "%i" /usr/bin/foo', 'stat -L -c "%i" %{_bindir}/foo'),
    ('stat --format=%Y /usr/bin/foo', 'stat --format=%Y %{_bindir}/foo'),
    # the git shield's format group reaches over the stat placeholder
    (
        'test "$(stat --format=%a %{buildroot}%{_bindir}/git)" = 755',
        'test "$(stat --format=%a %{buildroot}%{_bindir}/git)" = 755',
    ),
]


@pytest.mark.parametrize(('line', 'expected'), EMBRACE_STAT_FORMATS)
def test_embrace_leaves_stat_format_directives(
    default_options: Callable[..., dict[str, Any]], line: str, expected: str
) -> None:
    """%-directives in a stat -c/--format argument stay unbraced."""
    assert _cleaned_line(default_options, False, line) == expected


# gh#522: git log/show/for-each-ref --format/--pretty/--date=format:
# carries %-placeholders (%H, %h, %s, %an, %cd, ...) that belong to git,
# not to rpm.
EMBRACE_GIT_FORMATS = [
    (
        "%define git_version %(git log '-n1' '--date=format:%Y%m%d' "
        '\'--no-show-signature\' "--pretty=format:+git%cd.%h")',
        "%define git_version %(git log '-n1' '--date=format:%Y%m%d' "
        '\'--no-show-signature\' "--pretty=format:+git%cd.%h")',
    ),
    # the date shield runs first, and the git shield wraps its placeholder
    (
        'git log -1 --date=format:"+%Y" --format=%cd',
        'git log -1 --date=format:"+%Y" --format=%cd',
    ),
]


@pytest.mark.parametrize(('line', 'expected'), EMBRACE_GIT_FORMATS)
def test_embrace_leaves_git_format_placeholders(
    default_options: Callable[..., dict[str, Any]], line: str, expected: str
) -> None:
    """%-placeholders in a git --format/--pretty argument stay unbraced."""
    assert _cleaned_line(default_options, False, line) == expected


# gh#524: the program argument of awk(1) (gawk, mawk) carries %-forms
# (regex literals matching spec text like %lang(...), printf formats,
# strftime formats) that belong to awk, not to rpm.
EMBRACE_AWK_PROGRAMS = [
    # the reported case: %lang inside the regex, %buildroot outside it
    (
        "awk -v P=%buildroot '/^(%lang|[^%])/{print P $NF}' libpq.files libecpg.files | xargs rm",
        "awk -v P=%{buildroot} '/^(%lang|[^%])/{print P $NF}' libpq.files libecpg.files | xargs rm",
    ),
    # a '#' inside the program is not a comment
    ('awk \'/%lang/ {print "#"}\' f', 'awk \'/%lang/ {print "#"}\' f'),
    # a printf format inside the program stays unbraced too
    (
        'awk -F. \'{ printf "%d.%03d%03d", $1, $2, $3 }\'',
        'awk -F. \'{ printf "%d.%03d%03d", $1, $2, $3 }\'',
    ),
    # gawk and mawk take the same shield
    (
        "gawk '/^(%lang|[^%])/{print}' file",
        "gawk '/^(%lang|[^%])/{print}' file",
    ),
    (
        "mawk -v x=%foo '/%bar/{print}'",
        "mawk -v x=%{foo} '/%bar/{print}'",
    ),
    # a double-quoted program is shielded as well
    (
        'awk "/^(%lang|[^%])/ {print}"',
        'awk "/^(%lang|[^%])/ {print}"',
    ),
    # a quoted field separator is an option, not the program
    (
        "awk -F '[<>]' '/%lang/{print}'",
        "awk -F '[<>]' '/%lang/{print}'",
    ),
    (
        'awk -F " - " \'/%lang/{print}\'',
        'awk -F " - " \'/%lang/{print}\'',
    ),
    # a quoted value attached to the short option is an option too
    (
        "awk -F'[<>]' '/%lang/{print}'",
        "awk -F'[<>]' '/%lang/{print}'",
    ),
    # long options, with the value attached or separate
    (
        "awk --field-separator=: '/%lang/{print}'",
        "awk --field-separator=: '/%lang/{print}'",
    ),
    (
        "awk --field-separator : '/%lang/{print}'",
        "awk --field-separator : '/%lang/{print}'",
    ),
    # a quoted long-option value is an option too, attached or separate
    (
        'awk --field-separator=":" \'/%lang/{print}\'',
        'awk --field-separator=":" \'/%lang/{print}\'',
    ),
    (
        'awk --field-separator ":" \'/%lang/{print}\'',
        'awk --field-separator ":" \'/%lang/{print}\'',
    ),
    # a macro-spelled awk is shielded the same way; the macro itself
    # expands to gawk in the util pass
    (
        "%{__awk} '/%lang/{print}'",
        "gawk '/%lang/{print}'",
    ),
    # a braced macro inside the program stays verbatim
    (
        'awk \'{print "%{name}"}\'',
        'awk \'{print "%{name}"}\'',
    ),
    # a bare macro outside the program is still braced
    (
        "awk '/%lang/{print}' /usr/share/foo",
        "awk '/%lang/{print}' %{_datadir}/foo",
    ),
    # no program argument, nothing to shield: macros brace normally
    (
        'awk -f %{SOURCE1} /usr/bin/foo',
        'awk -f %{SOURCE1} %{_bindir}/foo',
    ),
    # 'awk' inside another word is not the command
    (
        'echo awk-%name',
        'echo awk-%{name}',
    ),
]


@pytest.mark.parametrize(('line', 'expected'), EMBRACE_AWK_PROGRAMS)
def test_embrace_leaves_awk_program_directives(
    default_options: Callable[..., dict[str, Any]], line: str, expected: str
) -> None:
    """%-forms in an awk program argument stay unbraced."""
    assert _cleaned_line(default_options, False, line) == expected


EMBRACE_FORMAT_LINES = [
    line
    for table in (
        EMBRACE_PRINTF_FORMATS,
        EMBRACE_SHELL_PRINTF_FORMATS,
        EMBRACE_DATE_FORMATS,
        EMBRACE_STAT_FORMATS,
        EMBRACE_GIT_FORMATS,
        EMBRACE_AWK_PROGRAMS,
    )
    for line, _ in table
]


@pytest.mark.parametrize('line', EMBRACE_FORMAT_LINES)
def test_embrace_never_leaves_placeholders(
    default_options: Callable[..., dict[str, Any]], line: str
) -> None:
    """No shield placeholder survives into the output, however the shields overlap."""
    assert '\x00' not in _cleaned_line(default_options, False, line)


def test_embrace_leaves_known_macro_function_unbraced(
    default_options: Callable[..., dict[str, Any]],
) -> None:
    """A macro function (an rpm builtin here) keeps its space separated arguments."""
    options = RpmSpecCleaner(default_options()).options
    options['defined_macros'] = set()
    section = Section(options)
    section.reg = Regexp(['global', 'gsub'])
    line = '%global llvm_major %gsub %{llvm_version} %{quote:%..+} %{quote: }'
    section.add(line)
    assert section.lines[0] == line


def test_embrace_skips_lua_body_lines(default_options: Callable[..., dict[str, Any]]) -> None:
    """%-forms inside a multiline %{lua: ... } body are lua text, not macro references."""
    section = _section(default_options, set())
    lines = [
        '%global _pyver %{lua: \\',
        '  local ver = string.sub(rpm.expand("%python"), string.len("python") + 1, -1); \\',
        '    print(string.format("%s.%s", string.sub(ver, 1, 1), string.sub(ver, 2, -1))); \\',
        '  print(rpm.expand("%{_bindir}/python%_pyver")); \\',
        '}',
    ]
    for line in lines:
        section.add(line)
    assert section.lines == lines
    # the state ends with the body: the next line is cleaned again
    section.add('Name: %name')
    assert section.lines[-1] == 'Name: %{name}'


def test_embrace_skips_single_line_lua_body(default_options: Callable[..., dict[str, Any]]) -> None:
    """A lua body closed on the same line shields only its own text."""
    section = _section(default_options, set())
    section.add('%global x %{lua: print("%s")} suffix %name')
    assert section.lines[0] == '%global x %{lua: print("%s")} suffix %{name}'


def test_embrace_skips_lua_body_shell_expansion(
    default_options: Callable[..., dict[str, Any]],
) -> None:
    """A shell expansion with nested parens inside a lua body is left verbatim."""
    section = _section(default_options, set())
    lines = [
        '%global _host_cpu %{lua: \\',
        '  local out = rpm.expand("%(echo (nested) done)"); \\',
        '  print(string.format("%s", out)); \\',
        '}',
    ]
    for line in lines:
        section.add(line)
    assert section.lines == lines
    # the state ends with the body: the next line is cleaned again
    section.add('Name: %name')
    assert section.lines[-1] == 'Name: %{name}'


def test_embrace_skips_lua_space_form(default_options: Callable[..., dict[str, Any]]) -> None:
    """In the %lua space form the arguments go to lua; they are lua text, not macro references."""
    section = _section(default_options, set())
    section.add('%global x %lua print("%s")')
    assert section.lines[0] == '%global x %lua print("%s")'
    # the arguments end with the line: the next line is cleaned again
    section.add('Name: %name')
    assert section.lines[-1] == 'Name: %{name}'


def test_embrace_skips_lua_space_form_with_macro_expansion(
    default_options: Callable[..., dict[str, Any]],
) -> None:
    """A %{...} the %lua arguments close does not end their shielding early."""
    line = '%global x %lua print("%{name}") .. "%s"'
    section = _section(default_options, set())
    section.add(line)
    assert section.lines[0] == line


def test_embrace_skips_lua_body_with_spaced_colon(
    default_options: Callable[..., dict[str, Any]],
) -> None:
    """The %{lua : form with whitespace before the colon is dispatched as well."""
    section = _section(default_options, set())
    section.add('%global x %{lua : print("%s")} suffix %name')
    assert section.lines[0] == '%global x %{lua : print("%s")} suffix %{name}'


def test_embrace_escaped_percent_lua_is_no_opener(
    default_options: Callable[..., dict[str, Any]],
) -> None:
    """%% is an escaped percent: %%{lua: is literal text and opens no body."""
    section = _section(default_options, set())
    section.add('echo 100%%{lua: x')
    assert section.lines[0] == 'echo 100%%{lua: x'
    # no body was opened, so the next line is cleaned again
    section.add('cp %name %version')
    assert section.lines[-1] == 'cp %{name} %{version}'


def test_embrace_lua_opener_in_comment_opens_nothing(
    default_options: Callable[..., dict[str, Any]],
) -> None:
    """An opener behind the # boundary braces no comment text and leaks no body state."""
    section = _section(default_options, set())
    section.add('echo %name # %{lua: } %version')
    assert section.lines[0] == 'echo %{name} # %{lua: } %version'
    # an unclosed opener in a trailing comment leaves no state behind either
    section.add('echo done # %{lua: print(')
    assert section.lines[-1] == 'echo done # %{lua: print('
    section.add('cp %name %version')
    assert section.lines[-1] == 'cp %{name} %{version}'
    # the same holds on the slow path, behind a body closed earlier on the line
    section.add('%{lua: print("x")} echo %name # %{lua: } %version')
    assert section.lines[-1] == '%{lua: print("x")} echo %{name} # %{lua: } %version'
    section.add('%{lua: print("x")} echo done # %{lua: print(')
    assert section.lines[-1] == '%{lua: print("x")} echo done # %{lua: print('
    section.add('cp %name %version')
    assert section.lines[-1] == 'cp %{name} %{version}'


def test_vendored_invocation_survives_full_run(
    default_options: Callable[..., dict[str, Any]], monkeypatch: pytest.MonkeyPatch
) -> None:
    """A function from the vendored snapshot keeps its invocation form through the full run."""
    monkeypatch.setattr('spec_cleaner.rpmcleaner.load_macro_functions', lambda: ['lang_package'])
    assert (
        _cleaned_line(default_options, False, '%lang_package(cryptsetup)')
        == '%lang_package(cryptsetup)'
    )
    assert _cleaned_line(default_options, False, '%lang_package foo') == '%lang_package foo'


def test_undetected_invocation_is_left_alone_in_full_run(
    default_options: Callable[..., dict[str, Any]], monkeypatch: pytest.MonkeyPatch
) -> None:
    """A function no source reports keeps its invocation form; only bare references are braced."""
    monkeypatch.setattr('spec_cleaner.rpmcleaner.load_macro_functions', lambda: [])
    assert _cleaned_line(default_options, False, '%other_macro(x)') == '%other_macro(x)'
    assert _cleaned_line(default_options, False, 'echo %frobnicate') == 'echo %{frobnicate}'


OPTFLAGS_QUOTED_USES = [
    # a bare use inside single quotes is literal text, not the flags
    ("echo '$RPM_OPT_FLAGS'", "echo '$RPM_OPT_FLAGS'"),
    # inside double quotes the shell expands it, so it is rewritten
    ('echo "$RPM_OPT_FLAGS"', 'echo "%{optflags}"'),
    # an assignment value inside single quotes is the template form
    # the quoting fixtures pin, so it is rewritten
    (
        "echo 'CFLAGS=$RPM_OPT_FLAGS -fPIC' >> config.mk",
        "echo 'CFLAGS=%{optflags} -fPIC' >> config.mk",
    ),
    (
        "sed -i 's|^CFLAGS = .*|CFLAGS = $RPM_OPT_FLAGS -fPIC|' Makefile",
        "sed -i 's|^CFLAGS = .*|CFLAGS = %{optflags} -fPIC|' Makefile",
    ),
    # an unquoted bare use is rewritten
    ('echo $RPM_OPT_FLAGS', 'echo %{optflags}'),
    # a comparison operator inside single quotes is literal text: the
    # shell expands neither side, so the '=' inside '==', '!=', '>=' or
    # '<=' is not an assignment and is left alone
    ("echo 'a == $RPM_OPT_FLAGS'", "echo 'a == $RPM_OPT_FLAGS'"),
    ("echo 'x != $RPM_OPT_FLAGS'", "echo 'x != $RPM_OPT_FLAGS'"),
    ("echo 'y >= $RPM_OPT_FLAGS'", "echo 'y >= $RPM_OPT_FLAGS'"),
    ("echo 'z <= $RPM_OPT_FLAGS'", "echo 'z <= $RPM_OPT_FLAGS'"),
    ("echo 'a == ${RPM_OPT_FLAGS}'", "echo 'a == ${RPM_OPT_FLAGS}'"),
    # a lone '=' stays an assignment value and is still rewritten
    (
        "echo 'CFLAGS=${RPM_OPT_FLAGS}'",
        "echo 'CFLAGS=%{optflags}'",
    ),
    # flags may precede the variable in the assignment value
    (
        "echo 'CFLAGS=-fPIC $RPM_OPT_FLAGS' >> config.mk",
        "echo 'CFLAGS=-fPIC %{optflags}' >> config.mk",
    ),
    (
        "echo 'CFLAGS=-fPIC ${RPM_OPT_FLAGS}' >> config.mk",
        "echo 'CFLAGS=-fPIC %{optflags}' >> config.mk",
    ),
    (
        "echo 'CFLAGS = -fPIC $RPM_OPT_FLAGS' >> config.mk",
        "echo 'CFLAGS = -fPIC %{optflags}' >> config.mk",
    ),
    # a second variable in the same assignment value is rewritten too
    (
        "echo 'CFLAGS=-fPIC $RPM_OPT_FLAGS ${RPM_OPT_FLAGS}'",
        "echo 'CFLAGS=-fPIC %{optflags} %{optflags}'",
    ),
    # a comparison after the flags still excludes the variable
    (
        "echo 'CFLAGS=-fPIC a == $RPM_OPT_FLAGS'",
        "echo 'CFLAGS=-fPIC a == $RPM_OPT_FLAGS'",
    ),
    (
        "echo 'CFLAGS=-fPIC x != $RPM_OPT_FLAGS'",
        "echo 'CFLAGS=-fPIC x != $RPM_OPT_FLAGS'",
    ),
    # a doubled comparison operator is still no assignment
    (
        "echo 'a === $RPM_OPT_FLAGS'",
        "echo 'a === $RPM_OPT_FLAGS'",
    ),
    (
        "echo 'a !== $RPM_OPT_FLAGS'",
        "echo 'a !== $RPM_OPT_FLAGS'",
    ),
]


@pytest.mark.parametrize(('line', 'expected'), OPTFLAGS_QUOTED_USES)
def test_replace_optflags_respects_quoting(
    default_options: Callable[..., dict[str, Any]], line: str, expected: str
) -> None:
    """$RPM_OPT_FLAGS is rewritten only where the shell would expand it."""
    assert _cleaned_line(default_options, False, line) == expected


def test_replace_optflags_skips_quoted_heredoc_body(
    default_options: Callable[..., dict[str, Any]],
) -> None:
    """A quoted heredoc delimiter suppresses expansion in its body."""
    section = _section(default_options, set())
    lines = [
        "cat > script.sh <<'EOF'",
        'CFLAGS=$RPM_OPT_FLAGS',
        'EOF',
        'cat > config.mk <<EOF',
        'CFLAGS = $RPM_OPT_FLAGS -fPIC',
        'EOF',
    ]
    for line in lines:
        section.add(line)
    assert section.lines == [
        "cat > script.sh <<'EOF'",
        'CFLAGS=$RPM_OPT_FLAGS',
        'EOF',
        'cat > config.mk <<EOF',
        'CFLAGS = %{optflags} -fPIC',
        'EOF',
    ]


def test_replace_optflags_ignores_heredoc_opener_inside_quotes(
    default_options: Callable[..., dict[str, Any]],
) -> None:
    """A heredoc spelling inside double quotes starts no heredoc body."""
    section = _section(default_options, set())
    lines = [
        'echo "usage: cat <<\'EOF\'"',
        'CFLAGS=$RPM_OPT_FLAGS',
        'CXXFLAGS=$RPM_OPT_FLAGS',
        'EOF',
    ]
    for line in lines:
        section.add(line)
    assert section.lines == [
        'echo "usage: cat <<\'EOF\'"',
        'CFLAGS="%{optflags}"',
        'CXXFLAGS="%{optflags}"',
        'EOF',
    ]


def test_replace_optflags_assignment_midline_forms(
    default_options: Callable[..., dict[str, Any]],
) -> None:
    """
    An assignment need not start the line to mark the variable.

    After a separator, in an environment prefix, or after 'env' it
    still marks the variable. A use that is no assignment (an argument,
    or an assignment to another variable) does not.
    """

    def _cleaned(lines: list[str]) -> list[str]:
        section = _section(default_options, set())
        for line in lines:
            section.add(line)
        return section.lines

    # compound assignments after a command separator
    for separator in (';', '&&', '||'):
        assert _cleaned(
            [
                f'FOO=1{separator} RPM_OPT_FLAGS="$RPM_OPT_FLAGS -x"',
                'CFLAGS="$RPM_OPT_FLAGS"',
            ]
        ) == [
            f'FOO=1{separator} RPM_OPT_FLAGS="$RPM_OPT_FLAGS -x"',
            'CFLAGS="$RPM_OPT_FLAGS"',
        ]
    # 'export' after a separator, and '+=' after a separator
    assert _cleaned(
        [
            'FOO=1; export RPM_OPT_FLAGS="$RPM_OPT_FLAGS -x"',
            'CFLAGS="$RPM_OPT_FLAGS"',
        ]
    ) == [
        'FOO=1; export RPM_OPT_FLAGS="$RPM_OPT_FLAGS -x"',
        'CFLAGS="$RPM_OPT_FLAGS"',
    ]
    assert _cleaned(
        [
            'FOO=1; RPM_OPT_FLAGS+=" -x"',
            'CFLAGS="$RPM_OPT_FLAGS"',
        ]
    ) == [
        'FOO=1; RPM_OPT_FLAGS+=" -x"',
        'CFLAGS="$RPM_OPT_FLAGS"',
    ]
    # in an environment prefix before the command, optionally led by
    # 'export', or after the 'env' command, or after a separator
    assert _cleaned(
        [
            'CFLAGS="-O2" RPM_OPT_FLAGS="$RPM_OPT_FLAGS -x" make',
            'CFLAGS="$RPM_OPT_FLAGS"',
        ]
    ) == [
        'CFLAGS="-O2" RPM_OPT_FLAGS="$RPM_OPT_FLAGS -x" make',
        'CFLAGS="$RPM_OPT_FLAGS"',
    ]
    assert _cleaned(
        [
            'export FOO=1 RPM_OPT_FLAGS="$RPM_OPT_FLAGS -x"',
            'CFLAGS="$RPM_OPT_FLAGS"',
        ]
    ) == [
        'export FOO=1 RPM_OPT_FLAGS="$RPM_OPT_FLAGS -x"',
        'CFLAGS="$RPM_OPT_FLAGS"',
    ]
    assert _cleaned(
        [
            'env RPM_OPT_FLAGS="$RPM_OPT_FLAGS -x" make',
            'CFLAGS="$RPM_OPT_FLAGS"',
        ]
    ) == [
        'env RPM_OPT_FLAGS="$RPM_OPT_FLAGS -x" make',
        'CFLAGS="$RPM_OPT_FLAGS"',
    ]
    assert _cleaned(
        [
            'cd src; CFLAGS="-O2" RPM_OPT_FLAGS="$RPM_OPT_FLAGS -x" make',
            'CFLAGS="$RPM_OPT_FLAGS"',
        ]
    ) == [
        'cd src; CFLAGS="-O2" RPM_OPT_FLAGS="$RPM_OPT_FLAGS -x" make',
        'CFLAGS="$RPM_OPT_FLAGS"',
    ]
    # no assignment: an argument, an assignment to another variable,
    # a use after the command name, or a longer variable name
    for first in (
        'echo RPM_OPT_FLAGS=x',
        'FOO=RPM_OPT_FLAGS=x',
        'make RPM_OPT_FLAGS=x',
        'FOO=bar make RPM_OPT_FLAGS=x',
        'RPM_OPT_FLAGS_EXTRA=x',
    ):
        assert _cleaned(
            [
                first,
                'CFLAGS="$RPM_OPT_FLAGS"',
            ]
        ) == [
            first,
            'CFLAGS="%{optflags}"',
        ]


def test_replace_optflags_keeps_assigned_variable(
    default_options: Callable[..., dict[str, Any]],
) -> None:
    """Once the section assigns to RPM_OPT_FLAGS, its references read the filtered value."""
    section = _section(default_options, set())
    lines = [
        # a use before any assignment still reads the environment value
        'CFLAGS="$RPM_OPT_FLAGS"',
        # the assignment itself keeps its right-hand side as well
        'RPM_OPT_FLAGS="$RPM_OPT_FLAGS -U_FORTIFY_SOURCE"',
        # the filtering chain reads the value built up so far
        "RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-Wall//g'`",
        'RPM_OPT_FLAGS="${RPM_OPT_FLAGS//-O[s0-9]/-O}"',
        'CFLAGS="$RPM_OPT_FLAGS"',
    ]
    for line in lines:
        section.add(line)
    assert section.lines == [
        'CFLAGS="%{optflags}"',
        'RPM_OPT_FLAGS="$RPM_OPT_FLAGS -U_FORTIFY_SOURCE"',
        "RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-Wall//g'`",
        'RPM_OPT_FLAGS="${RPM_OPT_FLAGS//-O[s0-9]/-O}"',
        'CFLAGS="$RPM_OPT_FLAGS"',
    ]


def test_replace_optflags_assignment_forms(
    default_options: Callable[..., dict[str, Any]],
) -> None:
    """'export' and '+=' assign the variable; a bare export and 'VAR = ...' do not."""

    def _cleaned(lines: list[str]) -> list[str]:
        section = _section(default_options, set())
        for line in lines:
            section.add(line)
        return section.lines

    # 'export' and '+=' are assignments too, indented or not
    assert _cleaned(
        [
            'export RPM_OPT_FLAGS="$RPM_OPT_FLAGS -std=gnu11"',
            'CFLAGS="$RPM_OPT_FLAGS"',
        ]
    ) == [
        'export RPM_OPT_FLAGS="$RPM_OPT_FLAGS -std=gnu11"',
        'CFLAGS="$RPM_OPT_FLAGS"',
    ]
    assert _cleaned(
        [
            'RPM_OPT_FLAGS+=" -Wno-error"',
            'CFLAGS="$RPM_OPT_FLAGS"',
        ]
    ) == [
        'RPM_OPT_FLAGS+=" -Wno-error"',
        'CFLAGS="$RPM_OPT_FLAGS"',
    ]
    assert _cleaned(
        [
            '\tRPM_OPT_FLAGS="$RPM_OPT_FLAGS -fPIC"',
            'CFLAGS="$RPM_OPT_FLAGS"',
        ]
    ) == [
        '\tRPM_OPT_FLAGS="$RPM_OPT_FLAGS -fPIC"',
        'CFLAGS="$RPM_OPT_FLAGS"',
    ]
    # a bare 'export' marks the variable for export without assigning it
    assert _cleaned(
        [
            'export RPM_OPT_FLAGS',
            'CFLAGS="$RPM_OPT_FLAGS"',
        ]
    ) == [
        'export RPM_OPT_FLAGS',
        'CFLAGS="%{optflags}"',
    ]
    # spaces around '=' make it a command invocation, not an assignment
    # (the trailing variable is still quoted and rewritten as usual)
    assert _cleaned(
        [
            'RPM_OPT_FLAGS = $RPM_OPT_FLAGS',
            'CFLAGS="$RPM_OPT_FLAGS"',
        ]
    ) == [
        'RPM_OPT_FLAGS ="%{optflags}"',
        'CFLAGS="%{optflags}"',
    ]
