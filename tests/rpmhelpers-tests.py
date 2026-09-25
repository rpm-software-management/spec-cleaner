#!/usr/bin/env python

import pytest

from spec_cleaner import RpmExceptionError, rpmhelpers


class TestRpmhelpers:
    """We run few tests to ensure rpmhelpers functions work fine."""

    def test_parse_rpm_showrc_locale_charset(self, monkeypatch):
        """Test parsing 'rpm --showrc' output printed in a non-UTF-8 locale (cs_CZ)."""
        output = b'-13: __apply_patch(qp:m:)\t\n==== aktivn\xed 1073 pr\xe1zdn\xe9 0\n'
        monkeypatch.setattr(rpmhelpers, 'check_output', lambda cmd: output)
        assert rpmhelpers.parse_rpm_showrc() == ['__apply_patch']

    def test_parse_rpm_showrc_missing_rpm(self, monkeypatch):
        """Test that a missing rpm binary is reported as RpmExceptionError."""

        def missing(cmd):
            raise FileNotFoundError(2, 'No such file or directory', 'rpm')

        monkeypatch.setattr(rpmhelpers, 'check_output', missing)
        with pytest.raises(RpmExceptionError):
            rpmhelpers.parse_rpm_showrc()
