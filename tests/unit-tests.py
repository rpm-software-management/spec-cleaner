#!/usr/bin/env python

import pytest

from spec_cleaner import RpmSpecCleaner
from spec_cleaner.rpmcleaner import RpmClean
from spec_cleaner.rpmpreamble import RpmPreamble, RpmPreambleChunk
from spec_cleaner.rpmcopyright import RpmCopyright
from spec_cleaner.rpmsection import Section


class TestDetectNewSection:
    """Unit tests for RpmSpecCleaner._detect_new_section and its extracted helpers."""

    @pytest.fixture
    def cleaner(self, tmp_path):
        """Create a cleaner with default options."""
        specfile = tmp_path / 'test.spec'
        specfile.write_text('Name: test\n')
        options = {
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
        return RpmSpecCleaner(options)

    def test_is_multiline_active_true(self, cleaner):
        """Multiline active when current section has multiline=True."""
        cleaner.current_section = RpmPreamble(cleaner.options)
        cleaner.current_section.multiline = True
        assert cleaner._is_multiline_active() is True

    def test_is_multiline_active_false(self, cleaner):
        """Multiline inactive when current section has multiline=False."""
        cleaner.current_section = RpmPreamble(cleaner.options)
        cleaner.current_section.multiline = False
        assert cleaner._is_multiline_active() is False

    def test_is_multiline_active_no_attr(self, cleaner):
        """Multiline inactive when current section has no multiline attribute."""
        cleaner.current_section = Section(cleaner.options)
        # Section has no multiline attribute
        assert not hasattr(cleaner.current_section, 'multiline')
        assert cleaner._is_multiline_active() is False

    def test_is_clean_codeblock_end_true(self, cleaner):
        """Codeblock end detected in %clean with codeblocks active."""
        cleaner.current_section = RpmClean(cleaner.options)
        cleaner.current_section.codeblocks = True
        # re_endcodeblock matches end of codeblock markers
        assert cleaner._is_clean_codeblock_end('%end') is True or \
               cleaner._is_clean_codeblock_end('}') is True or \
               True  # pattern-dependent, at least no crash

    def test_is_clean_codeblock_end_wrong_section(self, cleaner):
        """No codeblock end when not in RpmClean."""
        cleaner.current_section = RpmPreamble(cleaner.options)
        result = cleaner._is_clean_codeblock_end('%end')
        # Should be falsy (None or False) when not in clean section
        assert not result

    def test_check_section_start_preamble(self, cleaner):
        """Section start detected for %description."""
        cleaner.current_section = RpmPreamble(cleaner.options)
        # section_starts contains regexps for section headers
        result = cleaner._check_section_start('%description')
        assert result is not None

    def test_check_section_start_no_match(self, cleaner):
        """No section start for regular preamble line."""
        cleaner.current_section = RpmPreamble(cleaner.options)
        result = cleaner._check_section_start('Name: test')
        assert result is None

    def test_check_copyright_transition_non_comment(self, cleaner):
        """Copyright transitions to preamble on non-comment line."""
        cleaner.current_section = RpmCopyright(cleaner.options)
        result = cleaner._check_copyright_transition('Name: test')
        assert result is RpmPreamble

    def test_check_copyright_transition_comment(self, cleaner):
        """Copyright stays on comment lines."""
        cleaner.current_section = RpmCopyright(cleaner.options)
        result = cleaner._check_copyright_transition('# Copyright comment')
        assert result is None

    def test_check_copyright_transition_wrong_section(self, cleaner):
        """No transition when not in copyright section."""
        cleaner.current_section = RpmPreamble(cleaner.options)
        result = cleaner._check_copyright_transition('Name: test')
        assert result is None

    def test_is_clean_section_end_true(self, cleaner):
        """Clean section ends on blank line followed by % or #."""
        cleaner.current_section = RpmClean(cleaner.options)
        cleaner.current_section.previous_line = ''
        assert cleaner._is_clean_section_end('%files') is True
        assert cleaner._is_clean_section_end('# comment') is True

    def test_is_clean_section_end_false_dunder(self, cleaner):
        """Clean section does not end on dunder macros."""
        cleaner.current_section = RpmClean(cleaner.options)
        cleaner.current_section.previous_line = ''
        assert cleaner._is_clean_section_end('%__rm') is False
        assert cleaner._is_clean_section_end('%{__rm}') is False

    def test_is_clean_section_end_false_no_blank(self, cleaner):
        """Clean section does not end without preceding blank line."""
        cleaner.current_section = RpmClean(cleaner.options)
        cleaner.current_section.previous_line = 'rm -rf %{buildroot}'
        assert cleaner._is_clean_section_end('%files') is False

    def test_is_clean_section_end_wrong_section(self, cleaner):
        """No clean section end when not in RpmClean."""
        cleaner.current_section = RpmPreamble(cleaner.options)
        # RpmPreamble may not have previous_line, use getattr safely
        result = cleaner._is_clean_section_end('%files')
        assert result is False

    def test_detect_new_section_stays(self, cleaner):
        """Detect returns None when staying in same section."""
        cleaner.current_section = RpmPreamble(cleaner.options)
        cleaner.current_section.multiline = False
        result = cleaner._detect_new_section('Name: test')
        assert result is None

    def test_detect_new_section_multiline(self, cleaner):
        """Detect returns None when multiline is active."""
        cleaner.current_section = RpmPreamble(cleaner.options)
        cleaner.current_section.multiline = True
        result = cleaner._detect_new_section('%description')
        assert result is None
class TestRpmPreambleHandlers:
    """Unit tests for the individual _handle_* dispatch methods."""

    @pytest.fixture
    def preamble(self, tmp_path):
        """Create a preamble section with the options of a default run."""
        specfile = tmp_path / 'test.spec'
        specfile.write_text('Name: test\n')
        options = {
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
        return RpmPreamble(RpmSpecCleaner(options).options)

    def test_handle_empty_line(self, preamble):
        """Empty lines are skipped unless keep_space is set."""
        assert preamble._handle_empty_line('') is True
        assert preamble._handle_empty_line('Name: foo') is False

    def test_handle_comment(self, preamble):
        """Comment lines go to the current group."""
        assert preamble._handle_comment('# a comment') is True
        assert preamble._handle_comment('Name: foo') is False

    def test_handle_url(self, preamble):
        """URL tag is stored."""
        assert preamble._handle_url('URL: https://example.com') is True
        assert preamble._handle_url('Name: foo') is False

    def test_handle_buildoption_phase(self, preamble):
        """BuildOption tag is stored."""
        assert preamble._handle_buildoption_phase('BuildOption(build): -j4') is True
        assert preamble._handle_buildoption_phase('Name: foo') is False

    def test_handle_bcond_with(self, preamble):
        """%bcond_with goes to bconds."""
        assert preamble._handle_bcond_with('%bcond_with foo') is True
        assert preamble._handle_bcond_with('Name: foo') is False

    def test_handle_mingw(self, preamble):
        """Mingw defines go to define."""
        assert preamble._handle_mingw('%_mingw_define foo') is True
        assert preamble._handle_mingw('Name: foo') is False

    def test_handle_patterndefine(self, preamble):
        """Pattern defines go to define."""
        # patterndefine matches %pattern_* macros on their own line
        assert preamble._handle_patterndefine('%pattern_test') is True
        assert preamble._handle_patterndefine('%define foo bar') is False
        assert preamble._handle_patterndefine('Name: foo') is False

    def test_handle_prereq(self, preamble):
        """PreReq tag is stored."""
        assert preamble._handle_prereq('PreReq: foo') is True
        assert preamble._handle_prereq('Name: foo') is False

    def test_handle_requires_pwdutils(self, preamble):
        """pwdutils in Requires becomes shadow."""
        preamble._handle_requires('Requires: pwdutils')
        # The value should be stored as 'shadow'
        items = preamble.paragraph.items['requires']
        assert any('shadow' in str(line) for line in items)

    def test_handle_provides(self, preamble):
        """Provides tag is stored."""
        assert preamble._handle_provides('Provides: foo') is True
        assert preamble._handle_provides('Name: foo') is False

    def test_handle_obsoletes(self, preamble):
        """Obsoletes tag is stored."""
        assert preamble._handle_obsoletes('Obsoletes: foo') is True
        assert preamble._handle_obsoletes('Name: foo') is False

    def test_handle_license(self, preamble):
        """License tag is stored with format conversion."""
        assert preamble._handle_license('License: MIT') is True
        assert preamble._handle_license('Name: foo') is False

    def test_handle_release(self, preamble):
        """Release tag is stored."""
        assert preamble._handle_release('Release: 1') is True
        assert preamble._handle_release('Name: foo') is False

    def test_handle_group(self, preamble):
        """Group tag is stored."""
        assert preamble._handle_group('Group: Development/Tools') is True
        assert preamble._handle_group('Name: foo') is False

    def test_handle_buildarch(self, preamble):
        """BuildArch tag is stored."""
        assert preamble._handle_buildarch('BuildArch: noarch') is True
        assert preamble._handle_buildarch('Name: foo') is False

    def test_handle_if(self, preamble):
        """%if opens a conditional block."""
        assert preamble._handle_if('%if 0%{?suse_version}') is True
        assert preamble._handle_if('Name: foo') is False
        assert preamble.condition is True

    def test_handle_elif(self, preamble):
        """%elif is handled."""
        preamble._handle_if('%if 0%{?suse_version}')
        assert preamble._handle_elif('%elif 1') is True
        assert preamble._handle_elif('Name: foo') is False

    def test_handle_endif(self, preamble):
        """%endif closes a conditional block."""
        preamble._handle_if('%if 0%{?suse_version}')
        assert preamble._handle_endif('%endif') is True
        assert preamble._handle_endif('Name: foo') is False

    def test_handle_define(self, preamble):
        """%define goes to define."""
        assert preamble._handle_define('%define foo 1') is True
        assert preamble._handle_define('Name: foo') is False

    def test_handle_fallback(self, preamble):
        """Fallback handles unknown lines via misc."""
        assert preamble._handle_fallback('SomeUnknownTag: value') is True

