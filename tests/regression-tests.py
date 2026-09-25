"""
Regression tests for corpus robustness and idempotence fixes.

These cover real-world spec constructs that used to crash the cleaner or
produced output that changed on a second run.
"""

from spec_cleaner import RpmSpecCleaner
from spec_cleaner.dependency_parser import DependencyParser

OPTION_PRESETS = {
    'pkgconfig': True,
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

SPEC_TEMPLATE = """\
Name:           regression-test
Version:        1.0
Release:        0
Summary:        test
License:        BSD-3-Clause
{body}
%description
test

%files
"""


def run_cleaner(spec_text, tmp_path, name):
    """Run the cleaner once over spec_text, return the output text."""
    infile = tmp_path / f'{name}-in.spec'
    outfile = tmp_path / f'{name}-out.spec'
    infile.write_text(spec_text)
    options = dict(OPTION_PRESETS, specfile=str(infile), output=str(outfile))
    RpmSpecCleaner(options).run()
    return outfile.read_text()


def clean_twice(body, tmp_path, name):
    """Clean spec with the given preamble body twice, assert idempotence."""
    first = run_cleaner(SPEC_TEMPLATE.format(body=body), tmp_path, f'{name}-1')
    second = run_cleaner(first, tmp_path, f'{name}-2')
    assert first == second
    return first


class TestDependencyParserRobustness:
    """The dependency parser must accept real-world dependency constructs."""

    def test_caret_in_version(self):
        """Caret in a version (e.g. 8.0^fork) must not crash the parser."""
        tokens = DependencyParser('kchmviewer = 8.0^fork').flat_out()
        assert [(t.name, t.operator, t.version) for t in tokens] == [
            ('kchmviewer', '=', '8.0^fork')
        ]

    def test_conditional_macro(self):
        """Conditional macro references (e.g. %?foo) must not crash the parser."""
        tokens = DependencyParser('%?suse_sgx_gcc_major').flat_out()
        assert [t.name for t in tokens] == ['%?suse_sgx_gcc_major']

    def test_modalias_wildcards(self):
        """Question-mark wildcards in modalias strings must not crash the parser."""
        tokens = DependencyParser('modalias(mdio:0000000000110011100111??????????)').flat_out()
        assert [t.name for t in tokens] == ['modalias(mdio:0000000000110011100111??????????)']

    def test_empty_value_does_not_hang(self):
        """An empty dependency value must parse to nothing instead of hanging."""
        assert DependencyParser('').flat_out() == []
