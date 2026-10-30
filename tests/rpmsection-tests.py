from collections.abc import Callable
from typing import Any

import pytest

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
    assert len(KNOWN_DIR_MACROS) == 29


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
