#!/usr/bin/env python

import pytest

from spec_cleaner import RpmExceptionError
from spec_cleaner.rpmrequirestoken import RpmRequiresToken


class TestRpmRequiresToken:
    """We run few tests to ensure dependency tokens render the way rpm wants to read them."""

    @pytest.mark.parametrize(
        'operator, expected',
        [
            ('=<', '<='),
            ('=>', '>='),
            ('==', '='),
            ('>=', '>='),
            ('<=', '<='),
            ('=', '='),
            ('<', '<'),
            ('>', '>'),
        ],
    )
    def test_format_operator(self, operator, expected):
        """Test that the reversed spellings rpm refuses to parse are normalized."""
        token = RpmRequiresToken('foo', operator, '1', 'Requires:  ')
        assert str(token) == f'Requires:  foo {expected} 1'

    def test_packageand_macro_is_braced(self):
        """Test that a bare macro in packageand() is braced, the ':' shields it from the later expansion."""
        token = RpmRequiresToken('packageand(%name:foo)', None, None, 'Supplements: ')
        assert str(token) == 'Supplements: (%{name} and foo)'

    def test_name_without_version_or_operator(self):
        """Test that a bare name needs neither an operator nor a version to render."""
        assert str(RpmRequiresToken('foo', None, None, 'Requires:  ')) == 'Requires:  foo'

    def test_no_prefix_raises(self):
        """Test that a token that never got its tag cannot be rendered."""
        with pytest.raises(RpmExceptionError, match='^No defined prefix in RequiresToken'):
            str(RpmRequiresToken('foo', None, None, None))

    def test_no_name_raises(self):
        """Test that a token that lost its name is rejected instead of rendering a dangling operator."""
        with pytest.raises(RpmExceptionError, match='^No defined name in RequiresToken'):
            str(RpmRequiresToken('', None, None, 'Requires:  '))

    def test_version_without_operator_raises(self):
        """Test that a version without an operator is rejected instead of rendering a dangling version."""
        with pytest.raises(
            RpmExceptionError, match='^Have defined version and no operator or vice versa'
        ):
            str(RpmRequiresToken('foo', None, '1.0', 'Requires:  '))
