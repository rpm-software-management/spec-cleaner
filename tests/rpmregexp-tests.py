#!/usr/bin/env python

import time

from spec_cleaner.rpmregexp import Regexp


class TestRegexp:
    """We run few tests to ensure the regular expressions stay fast."""

    def test_long_rm_line(self) -> None:
        """Test that a long rm line without buildroot does not backtrack exponentially."""
        line = 'rm -rf ' + ' '.join(f'dir{i}' for i in range(20))
        start = time.perf_counter()
        assert not Regexp.re_clean.search(line)
        assert not Regexp.re_rm.search(line)
        assert time.perf_counter() - start < 1

    def test_re_if_only_real_directives(self) -> None:
        """Test that re_if matches only the real conditional directives."""
        for line in (
            '%if 0%{?suse_version}',
            '%ifarch x86_64',
            '%ifnarch ppc64',
            '%ifos linux',
            '%ifnos linux',
            '%if',
            '%{if 0%{?a}}',
            '%ifpython2',
            '%ifpython3',
            '%ifpython311',
            '%ifpypy3',
        ):
            assert Regexp.re_if.match(line), line
        for line in (
            '%iffy bar',
            '%ifdef foo',
            '%if0',
            '%if(0)',
            '%ifxyz',
            '%ifarchx',
            '%ifpythonx',
        ):
            assert not Regexp.re_if.match(line), line

    def test_re_multilinecond_closed_wrapper(self) -> None:
        """Test that a # comment holding the closing brace does not open a block."""
        for line in (
            '%{?with_foo: # comment}',
            '%{?with_foo: # }',
            '%{!?with_foo: # comment}',
        ):
            assert not Regexp.re_multilinecond.match(line), line
        for line in (
            '%{?with_foo:',
            '%{?with_foo: # comment',
            '%{!?with_foo: # note',
        ):
            assert Regexp.re_multilinecond.match(line), line

    def test_unbrace_keywords_case(self) -> None:
        """Test that section names unbrace in any case but other keywords only exactly."""
        reg = Regexp(['description', 'docdir', 'patch[0-9]*'])
        line = '%{Description} %{patch1} %{PATCH1} %{docdir} %{DOCDIR}'
        assert reg.re_unbrace_keywords.sub(r'%\1', line) == (
            '%Description %patch1 %{PATCH1} %docdir %{DOCDIR}'
        )

    def test_unbrace_keywords_glued(self) -> None:
        """Test that a use glued to a word character keeps its braces."""
        reg = Regexp(['description', 'docdir', 'patch[0-9]*'])
        unbrace = reg.re_unbrace_keywords.sub
        # glued to a letter or a digit the suffix would merge into
        # the macro name of the unbraced form
        assert unbrace(r'%\1', '%{docdir}foo') == '%{docdir}foo'
        assert unbrace(r'%\1', '%{patch0}2') == '%{patch0}2'
        assert unbrace(r'%\1', '%{Description}foo') == '%{Description}foo'
        # glued to a delimiter or closing the value it still unbraces
        assert unbrace(r'%\1', '%{docdir}/foo') == '%docdir/foo'
        assert unbrace(r'%\1', '%{patch0}-p1') == '%patch0-p1'
        assert unbrace(r'%\1', '%{docdir}') == '%docdir'

    def test_braced_argument_macro_contexts(self) -> None:
        """Test that only value-position uses of an argument-taking macro match."""
        reg = Regexp(['typelib'], ['typelib'])
        assert reg.re_braced_argument_macro is not None
        shielded = reg.re_braced_argument_macro.search
        # the following tokens belong to the surrounding grammar
        assert shielded('Requires: %{typelib} = %{version}')
        assert shielded('%files %{typelib} -f files.lang')
        assert shielded('Summary: the %{typelib} library files')
        # the closing quote of the value the use sits in
        assert shielded('optimize="%{typelib}"')
        # glued to a word character the suffix would merge into the
        # macro name of the unbraced form
        assert shielded('Requires: %{typelib}foo')
        # glued to a delimiter the use takes no arguments in either spelling
        assert not shielded('Name: ghc-%{typelib}')
        assert not shielded('Name: ghc-%{typelib}-devel')
        # closing the line the use takes no arguments either
        assert not shielded('%package -n %{typelib}')
        # an escaped percent is not a macro use at all
        assert not shielded('echo %%{typelib} = 1')
        # without argument-taking names nothing is shielded
        assert Regexp(['typelib']).re_braced_argument_macro is None

    def test_spec_prep_options(self) -> None:
        """Test that %prep with append/prepend options is recognised as a section."""
        prep = Regexp.re_spec_prep.match
        assert prep('%prep')
        assert prep('%prep -a')
        assert prep('%prep -p')
        assert prep('%prep -a 1')
        assert prep('%prep -p 1')
        assert prep('%prep -p /bin/sh')
        assert prep('%prep -a 1 -a 2')
        assert prep('%prep -p 1 -p 2')
        # '%setup' options are not '%prep' options: rpm rejects them
        assert not prep('%prep -n foo-1.0')
        assert not prep('%prep -nfoo-1.0')
        assert not prep('%prep -n foo -c')
        assert not prep('%prep -c')
        assert not prep('%prep -T')
        assert not prep('%prep -D')
        assert not prep('%prep -b 2')
        # attached arguments and mixed append/prepend are rejected by rpm
        assert not prep('%prep -a1')
        assert not prep('%prep -p1')
        assert not prep('%prep -a 1 -p 2')
        assert not prep('%prep -a -x')
        assert not prep('%prep -n -c')
        assert not prep('%prep foo')
        assert not prep('%preparation')

    def test_spec_prep_no_exponential_backtracking(self) -> None:
        """Test that long %prep option lines stay fast to match and reject."""
        line = '%prep' + ' -a 1' * 40
        start = time.perf_counter()
        assert Regexp.re_spec_prep.match(line)
        assert time.perf_counter() - start < 1
        line = '%prep' + ' -a' * 40 + ' -x'
        start = time.perf_counter()
        assert not Regexp.re_spec_prep.match(line)
        assert time.perf_counter() - start < 1

    def test_global_order_sensitive_spellings(self) -> None:
        """Test that ?/!/parameterised tag-macro spellings count as order sensitive."""
        sensitive = Regexp.re_global_order_sensitive.search
        assert sensitive('%global mydir %{name}-data')
        assert sensitive('%global mydir %{?name}-data')
        assert sensitive('%global mydir %{!name:foo}-data')
        assert sensitive('%global mydir %{name:foo}-data')
        assert sensitive('%global mydir %name-data')
        assert sensitive('%global mydir %{?version}-data')
        assert sensitive('%global mydir %{!release:1}-data')
        assert sensitive('%global mydir %{epoch:0}-data')
        assert not sensitive('%global mydir %{names}-data')
        assert not sensitive('%global mydir %{name2}-data')
        assert not sensitive('%global mydir %names-data')
        assert not sensitive('%global mydir %{foo}-data')

    def test_make_midline_and_path(self) -> None:
        """Test that make after another command or with a path matches."""
        make = Regexp.re_make.match
        assert make('make check')
        assert make('  make check')
        assert make('cd tests && make check')
        assert make('cd tests; make check')
        assert make('make all | tee build.log')
        assert make('/usr/bin/make check')
        assert make('/bin/make check')
        assert make('%{_bindir}/make check')
        assert make('%{bindir}/make check')
        assert make('%bindir/make check')
        assert make('cd tests && /usr/bin/make check')
        assert make('%{?_bindir}/make check')
        assert make('%?bindir/make check')
        assert make('%?_bindir/make check')
        assert make('%{?bindir}/make check')
        # separator-led make may itself be led by assignments
        assert make('cd tests && CFLAGS="-O2" make check')
        assert make("cd tests && CC=gcc CFLAGS='-O2 -g' make check")
        assert make('cd tests && CFLAGS="-O2" %{_bindir}/make check')
        # prose and lookalikes stay untouched (see make-env-prefix.spec)
        assert not make('echo make all')
        assert not make('echo "make all"')
        # a separator inside quotes or after a backslash is not a
        # command boundary, so make there stays an echo argument
        assert not make("echo 'run; make V=1 check'")
        assert not make('echo "run; make V=1 check"')
        assert not make('echo "a; make all"')
        assert not make('echo "a; make"')
        assert not make(r'echo foo\; make check')
        assert not make("echo 'run && make check'")
        assert not make('echo "run || make check"')
        # ... but a real separator after a quoted part still counts,
        # as do several real commands before make
        assert make("echo 'x' ; make check")
        assert make('echo "x" && make check')
        # a quoted make before a real separator stays quoted; only the
        # real command after it converts
        assert make('echo "a; make all"; make check')
        assert make('cd tests; cd src && make check')
        assert not make('grep -n make Makefile.in')
        assert not make('FOO=bar make all')
        assert not make('makefile: all')
        assert not make('cmake check')
        assert not make('xmake check')
        # the %make_build form matches the same prefix shapes
        build = Regexp.re_make_build.match
        assert build('%make_build check')
        assert build('cd tests && %make_build check')
        assert build('%{_bindir}/%make_build check')
        assert build('%{?_bindir}/%make_build check')
        assert build('cd tests && CFLAGS="-O2" %make_build check')
        assert not build('echo %make_build check')

    def test_make_first_call_wins(self) -> None:
        """Test that the first make call in a line is the one matched."""
        match = Regexp.re_make.match('make %{?_smp_mflags} || make')
        assert match is not None
        assert match.group(1) == ''
        assert match.group(2) == ''
        assert match.group(3) == ' %{?_smp_mflags} || make'
        match = Regexp.re_make.match('cd tests && make check; make test')
        assert match is not None
        assert match.group(1) == 'cd tests && '
        assert match.group(2) == ''
        assert match.group(3) == ' check; make test'
        match = Regexp.re_make.match('/usr/bin/make check')
        assert match is not None
        assert match.group(1) == ''
        assert match.group(2) == '/usr/bin/'
        assert match.group(3) == ' check'

    def test_make_already_converted_stays(self) -> None:
        """Test that a line whose first make is already %make_build is left alone."""
        make = Regexp.re_make.match
        assert not make('%make_build || make')
        assert not make('%make_build check')
        assert not make('cd tests && %make_build check')
        assert not make('cd tests && %make_build || make check')
        assert not make('cd tests && %make_build || CFLAGS="-O2" make check')

    def test_make_prefix_no_exponential_backtracking(self) -> None:
        """Test that a long separator-led line without make stays fast."""
        line = 'echo ' + '; '.join(f'foo{i}' for i in range(60)) + '; make check'
        start = time.perf_counter()
        assert Regexp.re_make.match(line)
        assert time.perf_counter() - start < 1
        line = 'echo ' + '; '.join(f'foo{i}' for i in range(60)) + '; done'
        start = time.perf_counter()
        assert not Regexp.re_make.match(line)
        assert time.perf_counter() - start < 1

    def test_make_separator_no_superlinear_backtracking(self) -> None:
        """Test that a long run of && separators stays fast."""
        line = '&&' * 14 + ' done'
        start = time.perf_counter()
        assert not Regexp.re_make.search(line)
        assert time.perf_counter() - start < 1
        start = time.perf_counter()
        assert not Regexp.re_make_build.search(line)
        assert time.perf_counter() - start < 1

    def test_tail_macros_conditional_and_glued(self) -> None:
        """Test that the conditional spelling counts as a tail macro and glued names do not."""
        tail = Regexp.re_tail_macros.match
        assert tail('%python_subpackages')
        assert tail('%{python_subpackages}')
        assert tail('%{?python_subpackages}')
        assert tail('%python_subpackages -a foo')
        assert tail('%{?python_subpackages} -a foo')
        assert not tail('%python_subpackagesfoo')
        assert not tail('%{python_subpackages}foo')
