# vim: set ts=4 sw=4 et: coding=UTF-8

import re
import os

from .fileutils import FileUtils

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
    output = os.popen('rpm --showrc')
    for line in output:
        line = line.rstrip('\n')
        found_macro = re_rc_macrofunc.sub(r'\1', line)
        if found_macro != line:
            macros += [found_macro]
    output.close()
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
