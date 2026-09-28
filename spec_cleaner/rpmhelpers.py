# vim: set ts=4 sw=4 et: coding=UTF-8

import re
from subprocess import CalledProcessError, check_output

from .fileutils import open_datafile, open_stringio_spec, stat_datafile
from .rpmexception import RpmExceptionError
from .rpmrequirestoken import RpmRequiresToken

# Per-process memo of data-file and showrc reads. Every RpmSpecCleaner
# parsed the same tables and forked the same `rpm --showrc` again, so one
# process cleaning many specs paid it all many times over. Entries are
# keyed by file identity and never evicted; the key space is a handful of
# shipped files times the versions seen, and a regenerated table simply
# misses under its new mtime. Only successes are stored: a missing file
# or a failing rpm still raises fresh on every call, exactly as before.
# Callers get a top-level copy, so sharing the cache cannot alias a list
# or dict one cleaner later rues.
_read_cache: dict = {}


def clear_read_caches() -> None:
    """
    Drop all memoized reads.

    Tests that mock check_output or open_datafile must call this first,
    or they observe the process-wide result instead of their mock.
    """
    _read_cache.clear()


LICENSES_CHANGES = 'licenses_changes.txt'
TEX_CONVERSIONS = 'tex_conversions.txt'
PKGCONFIG_CONVERSIONS = 'pkgconfig_conversions.txt'
PERL_CONVERSIONS = 'perl_conversions.txt'
CMAKE_CONVERSIONS = 'cmake_conversions.txt'
GROUPS_LIST = 'allowed_groups.txt'
BRACKETING_EXCLUDES = 'excludes-bracketing.txt'


def parse_rpm_showrc() -> list[str]:
    """
    Create a list of all macro functions in the 'rpm --showrc' output.

    Returns:
        A list of such macro functions.
    """
    if 'showrc' in _read_cache:
        return list(_read_cache['showrc'])
    macros: list[str] = []

    re_rc_macrofunc = re.compile(r'^-[0-9]+[:=]\s(\w+)\(.*')
    try:
        output = check_output(['rpm', '--showrc'])
    except (OSError, CalledProcessError) as error:
        raise RpmExceptionError(f'Could not run "rpm --showrc": {error}') from error
    # rpm prints in the locale charset; only ASCII macro names are needed
    for line in output.decode(errors='replace').split('\n'):
        found_macro = re_rc_macrofunc.sub(r'\1', line)
        if found_macro != line:
            macros += [found_macro]
    _read_cache['showrc'] = macros
    return list(macros)


def _cached_datafile(name: str, loader):
    """
    Run a data-file loader once per file identity, then replay the result.

    Args:
        name: The data file name, as passed to open_datafile.
        loader: A no-argument callable doing the actual read and parse.

    Returns:
        A top-level copy of the memoized result.
    """
    identity = stat_datafile(name)
    if identity is None:
        # no candidate exists, or the file layer is mocked away in a test:
        # never cache, so the error (or the mock) is produced fresh
        return loader()
    key = (name, identity)
    if key not in _read_cache:
        _read_cache[key] = loader()
    cached = _read_cache[key]
    return dict(cached) if isinstance(cached, dict) else list(cached)


def load_keywords_whitelist() -> list[str]:
    """
    Create a list of keywords contained in BRACKETING_EXCLUDES file (keywords that shouldn't be in brackets).

    Returns:
        A list of such keywords.
    """

    def load():
        with open_datafile(BRACKETING_EXCLUDES) as f:
            return [line.rstrip('\n') for line in f]

    return _cached_datafile(BRACKETING_EXCLUDES, load)


def find_macros_with_arg(spec: str) -> list[str]:
    """
    Create a list of all macro functions in the spec file.

    Args:
        spec: A string with the path to the specfile.

    Returns:
        A list of such macro functions.
    """
    macrofuncs: list[str] = []

    re_spec_macrofunc = re.compile(r'^\s*%(?:define|global)\s+(\w+)\(.*')
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

    def load():
        conversions = {}
        with open_datafile(conversion_file) as f:
            # the values are split by  ': '
            for number, line in enumerate(f, 1):
                fields = line.rstrip('\n').split(': ', 1)
                if len(fields) != 2:
                    raise RpmExceptionError(
                        f"Line {number} of {conversion_file} has no ': ' separator: {line.rstrip()!r}"
                    )
                key, value = fields
                names = value.split()
                # a package has one row per arch, keep only the names every row provides
                if key in conversions:
                    provided = set(names)
                    names = [i for i in conversions[key] if i in provided]
                conversions[key] = names
        return {key: ' '.join(names) for key, names in conversions.items() if names}

    return _cached_datafile(conversion_file, load)


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


def read_licenses_changes() -> dict[str, str]:
    """
    Create mapping of old licences to new licences.

    It uses LICENCES_CHANGES file that has the following format:

    correct license string<tab>known bad license string

    Tab is used as a separator. Lines starting with '#' are comments.

    Returns:
        A dict with the mapping.

    """

    def load():
        with open_datafile(LICENSES_CHANGES) as f:
            return {
                old: correct
                for correct, old in (
                    line.rstrip('\n').split('\t') for line in f if not line.startswith('#')
                )
            }

    return _cached_datafile(LICENSES_CHANGES, load)


def read_group_changes():
    """
    Read data for allowed groups.

    Returns:
        A list with allowed groups
    """

    def load():
        with open_datafile(GROUPS_LIST) as f:
            next(f)  # header starts with link where we find the groups
            return [line.rstrip('\n') for line in f]

    return _cached_datafile(GROUPS_LIST, load)


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
    # normalise the whitespace first, a separator may be followed or preceded by
    # it; one without an operand on either side is dropped, not turned into a
    # dangling AND/OR that no SPDX expression allows
    value = ' '.join(value.split()).strip('; ')
    # some known strings contain the separators split on below
    whole = value
    if whole in conversions:
        return conversions[whole]
    value = re_license_semicolon.sub(' and ', value)
    # split using 'or', 'and' and parenthesis, ignore empty strings
    licenses = []
    for a in re.split(r'(\(|\)| and | AND | OR | or (?!later)|;)', value):
        if a != '':
            licenses.append(a)
    if not licenses:
        licenses.append(value)

    for index, my_license in enumerate(licenses):
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
            # match the current and then based on wether the previous
            # value is a list we append or convert to list entirely
            idx = seen[marker]
            prev = result[idx]
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
                result[idx] = prev
            else:
                # Easy as there was no list
                # just replace it with our value
                result[idx] = item
            continue
        seen[marker] = len(result)
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
        raise RpmExceptionError(f'Unknown type of group in preamble: {type(group)}')


def open_macro_bodies(line: str, depth: tuple[int, int] = (0, 0)) -> tuple[int, int]:
    """
    Count the %{ and %( bodies left open after the line, as rpm does when joining spec lines.

    Args:
        line: A string representing a line to process.
        depth: The %{ and %( bodies open before the line.

    Returns:
        The %{ and %( bodies open after the line.
    """
    braces, parens = depth
    index = 0
    while index < len(line):
        char, following = line[index], line[index + 1 : index + 2]
        if char == '\\':
            # an escaped character never opens or closes a body
            index += 1
        elif char == '%' and following in ('%', '{', '('):
            index += 1
            if following == '{':
                braces += 1
            elif following == '(':
                parens += 1
        elif char in '{}' and braces:
            braces += 1 if char == '{' else -1
        elif char in '()' and parens:
            parens += 1 if char == '(' else -1
        index += 1
    return braces, parens


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
