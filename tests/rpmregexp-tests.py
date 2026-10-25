#!/usr/bin/env python

import time

from spec_cleaner.rpmregexp import Regexp


class TestRegexp:
    """We run few tests to ensure the regular expressions stay fast."""

    def test_long_rm_line(self):
        """Test that a long rm line without buildroot does not backtrack exponentially."""
        line = 'rm -rf ' + ' '.join(f'dir{i}' for i in range(20))
        start = time.perf_counter()
        assert not Regexp.re_clean.search(line)
        assert not Regexp.re_rm.search(line)
        assert time.perf_counter() - start < 1

    def test_unbrace_keywords_case(self):
        """Test that section names unbrace in any case but other keywords only exactly."""
        reg = Regexp(['description', 'docdir', 'patch[0-9]*'])
        line = '%{Description} %{patch1} %{PATCH1} %{docdir} %{DOCDIR}'
        assert reg.re_unbrace_keywords.sub(r'%\1', line) == (
            '%Description %patch1 %{PATCH1} %docdir %{DOCDIR}'
        )

    def test_braced_argument_macro_contexts(self):
        """Test that only value-position uses of an argument-taking macro match."""
        reg = Regexp(['typelib'], ['typelib'])
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
