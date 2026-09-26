"""
Shared test fixtures.

The acceptance and CLI tests run the full cleaner, which calls
'parse_rpm_showrc()' to learn macro functions from the host's rpm.
Mock it to an empty list so the suite runs on machines without
the rpm binary (e.g. macOS); tests that exercise parse_rpm_showrc
itself (rpmhelpers-tests.py) call it directly and are unaffected.
"""

import pytest


@pytest.fixture(autouse=True)
def _mock_rpm_showrc(monkeypatch):
    monkeypatch.setattr('spec_cleaner.rpmcleaner.parse_rpm_showrc', lambda: [])
