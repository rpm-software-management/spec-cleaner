#!/usr/bin/env python

import pytest

from spec_cleaner import RpmSpecCleaner
from spec_cleaner.rpmcleaner import RpmClean
from spec_cleaner.rpmcopyright import RpmCopyright
from spec_cleaner.rpmpreamble import RpmPreamble
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


class TestDetectNewSection:
    """Unit tests for RpmSpecCleaner._detect_new_section and its extracted helpers."""

    @pytest.fixture
    def cleaner(self, tmp_path):
        """Create a cleaner with default options."""
        return RpmSpecCleaner(_default_options(tmp_path))

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
        # re_endcodeblock matches manual section end markers
        assert cleaner._is_clean_codeblock_end('# /SECTION') is True
        assert cleaner._is_clean_codeblock_end('# MANUAL END') is True

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
        return RpmPreamble(RpmSpecCleaner(_default_options(tmp_path)).options)

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
        """Pwdutils in Requires becomes shadow."""
        preamble._handle_requires('Requires: pwdutils')
        # The value should be stored as 'shadow'
        items = preamble.paragraph.items['requires']
        assert len(items) == 1
        assert items[0].name == 'shadow'

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

    def test_handle_continued_condition(self, preamble):
        """Continued condition lines are appended."""
        preamble._handle_if('%if 0%{?suse_version} \\')
        assert preamble._handle_continued_condition('continued') is True
        assert preamble._handle_continued_condition('Name: foo') is False

    def test_handle_multiline(self, preamble):
        """Multiline define continuation is handled."""
        preamble.multiline = True
        preamble.paragraph.items['define'] = [[]]
        assert preamble._handle_multiline('continued line') is True
        preamble.multiline = False
        assert preamble._handle_multiline('Name: foo') is False

    def test_handle_source(self, preamble):
        """Source tag is stored."""
        assert preamble._handle_source('Source0: foo.tar.gz') is True
        assert preamble._handle_source('Name: foo') is False

    def test_handle_patch(self, preamble):
        """Patch tag is stored."""
        assert preamble._handle_patch('Patch0: foo.patch') is True
        assert preamble._handle_patch('Name: foo') is False

    def test_handle_patternprovides(self, preamble):
        """Pattern provides are stored."""
        assert preamble._handle_patternprovides('Provides: pattern() = foo') is True
        assert preamble._handle_patternprovides('Name: foo') is False

    def test_handle_patternrequires(self, preamble):
        """Pattern requires are stored."""
        assert preamble._handle_patternrequires('Requires: pattern() = foo') is True
        assert preamble._handle_patternrequires('Name: foo') is False

    def test_handle_summary_localized(self, preamble):
        """Localized summary is stored."""
        assert preamble._handle_summary_localized('Summary(de): foo') is True
        assert preamble._handle_summary_localized('Name: foo') is False

    def test_handle_head_macros(self, preamble):
        """Head macros are handled."""
        assert preamble._handle_head_macros('%sle15_python_module_pythons') is True
        assert preamble._handle_head_macros('Name: foo') is False


class TestEndSubparagraphHelpers:
    """Unit tests for the end_subparagraph extracted helpers."""

    @pytest.fixture
    def preamble(self, tmp_path):
        """Create a preamble section with the options of a default run."""
        return RpmPreamble(RpmSpecCleaner(_default_options(tmp_path)).options)

    def test_track_condition_flags_nvr(self, preamble):
        """NVR flag is set when name/version/release/epoch present."""
        preamble.paragraph.items['name'] = ['test']
        preamble._track_condition_flags()
        assert preamble._condition_nvr is True

    def test_track_condition_flags_define(self, preamble):
        """Define flag is set when defines present."""
        from spec_cleaner.rpmpreamble import MacroLine

        preamble.paragraph.items['define'] = [[MacroLine('%define foo 1')]]
        preamble._track_condition_flags()
        assert preamble._condition_define is True

    def test_get_sub_block_flags(self, preamble):
        """Sub block flags reflect bconds and defines."""
        preamble.paragraph.items['bconds'] = ['%bcond_with foo']
        has_bconds, has_defines = preamble._get_sub_block_flags()
        assert has_bconds is True
        assert has_defines is False

    def test_handle_unclosed_condition(self, preamble):
        """Unclosed conditions move to open_conditions."""
        preamble.paragraph.items['conditions'] = ['%if foo']
        preamble._handle_unclosed_condition()
        assert preamble.paragraph.items['open_conditions'] == ['%if foo']
        assert preamble.paragraph.items['conditions'] == []

    def test_restore_condition_flags(self, preamble):
        """Flags are restored from stacks."""
        preamble._bcond_stack = [True]
        preamble._define_stack = [True]
        # Non-empty oldstore prevents top-level reset
        preamble._oldstore = [preamble.paragraph]
        preamble._restore_condition_flags()
        assert preamble._condition_bcond is True
        assert preamble._condition_define is True

    def test_restore_condition_flags_top_level_reset(self, preamble):
        """Flags reset at top level when oldstore is empty."""
        preamble._condition_bcond = True
        preamble._condition_define = True
        preamble._oldstore = []
        preamble._restore_condition_flags()
        assert preamble._condition_bcond is False
        assert preamble._condition_define is False

    def test_handle_multilinecond_start(self, preamble):
        """Multiline conditional start is handled."""
        assert preamble._handle_multilinecond_start('%{?suse_version:') is True
        assert preamble._handle_multilinecond_start('Name: foo') is False
        assert preamble.condition is True

    def test_handle_patternobsoletes_provides(self, preamble):
        """Provides with pattern obsolete is stored."""
        assert preamble._handle_patternobsoletes_provides('Provides: patterns-openSUSE-foo') is True
        assert preamble._handle_patternobsoletes_provides('Provides: foo') is False
        assert preamble._handle_patternobsoletes_provides('Name: foo') is False

    def test_handle_patternrecommends(self, preamble):
        """Recommends with pattern macro is stored."""
        assert preamble._handle_patternrecommends('Recommends: pattern() = foo') is True
        assert preamble._handle_patternrecommends('Recommends: foo') is False
        assert preamble._handle_patternrecommends('Name: foo') is False

    def test_handle_patternsuggests(self, preamble):
        """Suggests with pattern macro is stored."""
        assert preamble._handle_patternsuggests('Suggests: pattern() = foo') is True
        assert preamble._handle_patternsuggests('Suggests: foo') is False
        assert preamble._handle_patternsuggests('Name: foo') is False

    def test_handle_patternobsoletes(self, preamble):
        """Obsoletes with pattern obsolete is stored."""
        assert preamble._handle_patternobsoletes('Obsoletes: patterns-openSUSE-foo') is True
        assert preamble._handle_patternobsoletes('Obsoletes: foo') is False
        assert preamble._handle_patternobsoletes('Name: foo') is False

    def test_handle_requires_eq(self, preamble):
        """Requires with = version is handled."""
        assert preamble._handle_requires_eq('%requires_eq foo 1.0') is True
        assert preamble._handle_requires_eq('Name: foo') is False

    def test_handle_requires_ge(self, preamble):
        """Requires with >= version is handled."""
        assert preamble._handle_requires_ge('%requires_ge foo 1.0') is True
        assert preamble._handle_requires_ge('Name: foo') is False

    def test_handle_onelinecond_dep(self, preamble):
        """One-line conditional dependency is handled."""
        assert preamble._handle_onelinecond_dep('%{?suse_version:BuildRequires: foo}') is True
        assert preamble._handle_onelinecond_dep('Name: foo') is False

    def test_handle_requires_phase(self, preamble):
        """Requires(phase) tag is handled."""
        assert preamble._handle_requires_phase('Requires(post): foo') is True
        assert preamble._handle_requires_phase('Name: foo') is False


class TestPlaceHelpers:
    """Unit tests for the condition block placement helpers."""

    @pytest.fixture
    def preamble(self, tmp_path):
        """Create a preamble section with the options of a default run."""
        return RpmPreamble(RpmSpecCleaner(_default_options(tmp_path)).options)

    def test_place_non_define_block(self, preamble):
        """Non-define condition block goes to build_conditions by default."""
        from spec_cleaner.rpmpreamble import MacroLine

        cond = MacroLine('%if foo', is_cond=True)
        preamble.paragraph.items['conditions'] = [cond]
        preamble._condition_nvr = False
        preamble._pattern_condition = False
        preamble._place_non_define_block()
        assert preamble.paragraph.items['build_conditions'] == [cond]

    def test_place_non_define_block_nvr(self, preamble):
        """NVR condition block goes to nvr_conditions."""
        from spec_cleaner.rpmpreamble import MacroLine

        cond = MacroLine('%if foo', is_cond=True)
        preamble.paragraph.items['conditions'] = [cond]
        preamble._condition_nvr = True
        preamble._pattern_condition = False
        preamble._place_non_define_block()
        # NVR without late macros goes to nvr_conditions
        assert cond in (
            preamble.paragraph.items['nvr_conditions']
            + preamble.paragraph.items['build_conditions']
        )

    def test_place_define_block(self, preamble):
        """Define condition block is placed without crash."""
        from spec_cleaner.rpmpreamble import MacroLine

        preamble.paragraph.items['conditions'] = [MacroLine('%if foo', is_cond=True)]
        preamble._condition_bcond = False
        # Should not crash
        preamble._place_define_block(False, True)

    def test_place_condition_block_dispatch(self, preamble):
        """Condition block dispatches based on define flag."""
        from spec_cleaner.rpmpreamble import MacroLine

        cond = MacroLine('%if foo', is_cond=True)
        preamble.paragraph.items['conditions'] = [cond]
        preamble._condition_define = False
        preamble._condition_nvr = False
        preamble._pattern_condition = False
        preamble._place_condition_block(False, False)
        assert preamble.paragraph.items['build_conditions'] == [cond]
