# vim: set ts=4 sw=4 et: coding=UTF-8

import re
from subprocess import check_output

from .fileutils import FileUtils
from .rpmexception import RpmException
from .rpmrequirestoken import RpmRequiresToken

LICENSES_CHANGES = 'licenses_changes.txt'
TEX_CONVERSIONS = 'tex_conversions.txt'
PKGCONFIG_CONVERSIONS = 'pkgconfig_conversions.txt'
PERL_CONVERSIONS = 'perl_conversions.txt'
CMAKE_CONVERSIONS = 'cmake_conversions.txt'
GROUPS_LIST = 'allowed_groups.txt'
BRACKETING_EXCLUDES = 'excludes-bracketing.txt'


def parse_rpm_showrc():
    macros = []

    re_rc_macrofunc = re.compile(r'^-[0-9]+[:=]\s(\w+)\(.*')
    output = check_output(['rpm', '--showrc'])
    for line in output.decode().split('\n'):
        found_macro = re_rc_macrofunc.sub(r'\1', line)
        if found_macro != line:
            macros += [found_macro]
    return macros


def load_keywords_whitelist():
    keywords = []

    files = FileUtils()
    files.open_datafile(BRACKETING_EXCLUDES)
    for line in files.f:
        keywords.append(line.rstrip('\n'))
    files.close()

    return keywords


def find_macros_with_arg(spec):
    macrofuncs = []

    re_spec_macrofunc = re.compile(r'^\s*%define\s(\w+)\(.*')
    files = FileUtils()
    files.open(spec, 'r')
    for line in files.f:
        line = line.rstrip('\n')
        found_macro = re_spec_macrofunc.sub(r'\1', line)
        if found_macro != line:
            macrofuncs += [found_macro]
    files.close()
    return macrofuncs


def read_conversion_changes(conversion_file):
    conversions = {}

    files = FileUtils()
    files.open_datafile(conversion_file)
    for line in files.f:
        # the values are split by  ': '
        pair = line.split(': ')
        conversions[pair[0]] = pair[1][:-1]
    files.close()
    return conversions


def read_tex_changes():
    return read_conversion_changes(TEX_CONVERSIONS)


def read_pkgconfig_changes():
    return read_conversion_changes(PKGCONFIG_CONVERSIONS)


def read_perl_changes():
    return read_conversion_changes(PERL_CONVERSIONS)


def read_cmake_changes():
    return read_conversion_changes(CMAKE_CONVERSIONS)


def read_licenses_changes():
    licenses = {}

    files = FileUtils()
    files.open_datafile(LICENSES_CHANGES)
    # Header starts with # first line so skip
    next(files.f)
    for line in files.f:
        # strip newline
        line = line.rstrip('\n')
        # file has format
        # correct license string<tab>known bad license string
        # tab is used as separator
        pair = line.split('\t')
        licenses[pair[1]] = pair[0]
    files.close()
    return licenses


def read_group_changes():
    groups = []

    files = FileUtils()
    files.open_datafile(GROUPS_LIST)
    # header starts with link where we find the groups
    next(files.f)
    for line in files.f:
        line = line.rstrip('\n')
        groups.append(line)
    files.close()
    return groups


def fix_license(value, conversions):
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
    s = ' '.join(licenses).replace("( ", "(").replace(" )", ")").replace(' and ', ' AND ').replace(' or ', ' OR ').replace(' with ', ' WITH ')
    return s


def sort_uniq(seq):
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
    """
    Flatten the lines of the group from sublits to one simple list
    """
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
        raise RpmException('Unknown type of group in preamble: %s' % type(group))


def find_pkgconfig_statement(elements):
    """
    Find pkgconfig() statement in the list and return true if matched
    """

    pkgconfig_found = find_pkgconfig_declaration(elements)
    for i in elements:
        if isinstance(i, RpmRequiresToken):
            if 'pkgconfig(' in i.name and not pkgconfig_found:
                return True
    return False


def find_pkgconfig_declaration(elements):
    """
    Find if there is direct pkgconfig dependency in the paragraph
    """
    for i in elements:
        if isinstance(i, RpmRequiresToken):
            if 'pkgconfig ' in i.name or i.name.endswith('pkgconfig'):
                return True
    return False
