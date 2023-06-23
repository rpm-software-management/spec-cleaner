# vim: set ts=4 sw=4 et: coding=UTF-8

import re
from subprocess import check_output
from typing import Dict, List

from .fileutils import open_datafile, open_stringio_spec
from .rpmexception import RpmExceptionError
from .rpmrequirestoken import RpmRequiresToken

LICENSES_CHANGES = 'licenses_changes.txt'
TEX_CONVERSIONS = 'tex_conversions.txt'
PKGCONFIG_CONVERSIONS = 'pkgconfig_conversions.txt'
PERL_CONVERSIONS = 'perl_conversions.txt'
CMAKE_CONVERSIONS = 'cmake_conversions.txt'
GROUPS_LIST = 'allowed_groups.txt'
BRACKETING_EXCLUDES = 'excludes-bracketing.txt'


def parse_rpm_showrc() -> List[str]:
    """
    Create a list of all macro functions in the 'rpm --showrc' output.

    Returns:
        A list of such macro functions.
    """
    macros: List[str] = []

    re_rc_macrofunc = re.compile(r'^-[0-9]+[:=]\s(\w+)\(.*')
    output = check_output(['rpm', '--showrc'])
    for line in output.decode().split('\n'):
        found_macro = re_rc_macrofunc.sub(r'\1', line)
        if found_macro != line:
            macros += [found_macro]
    return macros


def load_keywords_whitelist() -> List[str]:
    """
    Create a list of keywords contained in BRACKETING_EXCLUDES file (keywords that shouldn't be in brackets).

    Returns:
        A list of such keywords.
    """
    with open_datafile(BRACKETING_EXCLUDES) as f:
        return [line.rstrip('\n') for line in f]


def find_macros_with_arg(spec: str) -> List[str]:
    """
    Create a list of all macro functions in the spec file.

    Args:
        spec: A string with the path to the specfile.

    Returns:
        A list of such macro functions.
    """
    macrofuncs: List[str] = []

    re_spec_macrofunc = re.compile(r'^\s*%define\s(\w+)\(.*')
    with open_stringio_spec(spec) as f:
        for line in (i.rstrip('\n') for i in f):
            found_macro = re_spec_macrofunc.sub(r'\1', line)
            if found_macro != line:
                macrofuncs += [found_macro]
    return macrofuncs


def read_conversion_changes(conversion_file):
    """
    Read up the conversion file for the replacements.

    Args:
        conversion_file: File to load up the data

    Returns:
        A dictionary with old -> new values for conversion
    """
    with open_datafile(conversion_file) as f:
        # the values are split by  ': '
        return dict(line.split(': ') for line in f)


def read_tex_changes():
    """Read up the tex conversion types."""
    return read_conversion_changes(TEX_CONVERSIONS)


def read_pkgconfig_changes():
    """Read up the pkgconfig conversion types."""
    return read_conversion_changes(PKGCONFIG_CONVERSIONS)


def read_perl_changes():
    """Read up the perl conversion types."""
    return read_conversion_changes(PERL_CONVERSIONS)


def read_cmake_changes():
    """Read up the cmake conversion types."""
    return read_conversion_changes(CMAKE_CONVERSIONS)


def read_licenses_changes() -> Dict[str, str]:
    """
    Create mapping of old licences to new licences.

    It uses LICENCES_CHANGES file that has the following format:

    correct license string<tab>known bad license string

    Tab is used as a separator.

    Returns:
        A dict with the mapping.

    """
    with open_datafile(LICENSES_CHANGES) as f:
        next(f)  # strip newline
        return {old: correct for correct, old in (line.rstrip('\n').split('\t') for line in f)}


def read_group_changes():
    """
    Read data for allowed groups.

    Returns:
        A list with allowed groups
    """
    with open_datafile(GROUPS_LIST) as f:
        next(f)  # header starts with link where we find the groups
        return [line.rstrip('\n') for line in f]


def fix_license(value, conversions):
    """
    Fix license string to match up current SPDX format.

    Args:
        value: the current license string
        conversions: list of known license format replacements

    Returns:
        string with the new license
    """
    # license ; should be replaced by ands so find it
    re_license_semicolon = re.compile(r'\s*;\s*')
    value = value.rstrip(';')
    value = re_license_semicolon.sub(' and ', value)
    # split using 'or', 'and' and parenthesis, ignore empty strings
    licenses = []
    for a in re.split(r'(\(|\)| and | AND | OR | or (?!later)|;)', value):
        if a != '':
            licenses.append(a)
    if not licenses:
        licenses.append(value)

    for (index, my_license) in enumerate(licenses):
        my_license = ' '.join(my_license.split())
        my_license = my_license.replace('ORlater', 'or later')
        my_license = my_license.replace('ORsim', 'or similar')
        if my_license in conversions:
            my_license = conversions[my_license]
        licenses[index] = my_license

    # create back new string with replaced licenses
    s = (
        ' '.join(licenses)
        .replace('( ', '(')
        .replace(' )', ')')
        .replace(' and ', ' AND ')
        .replace(' or ', ' OR ')
        .replace(' with ', ' WITH ')
    )
    return s


def sort_uniq(seq):
    """
    Sort sequence.

    Args:
        seq: the sequence of the data

    Returns:
        sequence with sorted order and no duplicates
    """

    def _check_list(x):
        if isinstance(x, list):
            return True
        else:
            return False

    seen = {}
    result = []
    for item in seq:
        marker = item
        # We can have list there with comment
        # So if list found just grab latest in the sublist
        if _check_list(marker):
            marker = marker[-1]
        if marker in seen:
            # Not a list, no comment to preserve
            if not _check_list(item):
                continue
            # Here we need to preserve comment content
            # As the list is already sorted we can count on it to be
            # seen in previous run.
            # match the current and then based on wether the previous
            # value is a list we append or convert to list entirely
            prev = result[-1]
            if _check_list(prev):
                # Remove last line of the appending
                # list which is the actual dupe value
                item.pop()
                # Remove it from orginal
                prev.pop()
                # join together
                prev += item
                # append the value back
                prev.append(marker)
                result[-1] = prev
            else:
                # Easy as there was no list
                # just replace it with our value
                result[-1] = item
            continue
        seen[marker] = 1
        result.append(item)
    return result


def add_group(group):
    """Flatten the lines of the group from sublits to one simple list."""
    if isinstance(group, str):
        return [group]
    elif isinstance(group, RpmRequiresToken):
        items = []
        if group.comments:
            items += group.comments
        items.append(group)
        return items
    elif isinstance(group, list):
        items = []
        for subgroup in group:
            items += add_group(subgroup)
        return items
    else:
        raise RpmExceptionError('Unknown type of group in preamble: %s' % type(group))


def find_pkgconfig_statement(elements):
    """
    Find pkgconfig() statement.

    Args:
        elements: A list of items we want to scan.

    Returns:
        True if pkgconfig() statement was found (and pkgconfig declaration wasn't), False otherwise.
    """
    pkgconfig_found = find_pkgconfig_declaration(elements)
    for i in elements:
        if isinstance(i, RpmRequiresToken):
            if 'pkgconfig(' in i.name and not pkgconfig_found:
                return True
    return False


def find_pkgconfig_declaration(elements):
    """
    Find if there is direct pkgconfig dependency in the paragraph.

    Args:
        elements: A list of items we want to scan.

    Returns:
        True if a pkgconfig dependency was found, False otherwise.
    """
    for i in elements:
        if isinstance(i, RpmRequiresToken):
            if 'pkgconfig ' in i.name or i.name.endswith('pkgconfig'):
                return True
    return False
