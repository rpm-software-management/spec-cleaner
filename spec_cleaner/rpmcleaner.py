# vim: set ts=4 sw=4 et: coding=UTF-8

import os.path
import shlex
import subprocess
import sys
import tempfile
from typing import IO, Any, Dict, List, Optional, Type

from .fileutils import open_stringio_spec
from .rpmbuild import RpmBuild
from .rpmcheck import RpmCheck
from .rpmcopyright import RpmCopyright
from .rpmdescription import RpmDescription
from .rpmexception import RpmExceptionError
from .rpmfiles import RpmFiles
from .rpmhelpers import (
    find_macros_with_arg,
    load_keywords_whitelist,
    parse_rpm_showrc,
    read_cmake_changes,
    read_group_changes,
    read_licenses_changes,
    read_perl_changes,
    read_pkgconfig_changes,
    read_tex_changes,
)
from .rpminstall import RpmInstall
from .rpmpackage import RpmPackage
from .rpmpreamble import RpmPreamble
from .rpmprep import RpmPrep
from .rpmprune import RpmChangelog, RpmClean
from .rpmregexp import Regexp
from .rpmscriplets import RpmScriptlets
from .rpmsection import Section


class RpmSpecCleaner(object):
    """
    Class wrapping all sections parser is responsible for.

    It ensures that all sections are checked and accounted for.

    If the section is required and not found it is created with
    blank values as fixme for the spec creator.

    Attributes:
        specfile: A string with the path to the specfile to process.
        fin: An in-memory input stream with the input file data.
        fout: A file object representing output file.
        current_section: A Section object representing current section of spec file.
        skip_run: A bool indicating whether the cleaning of the specfile should be
                 skipped.
        options: A dictionary holding both spec-cleaner commandline arguments and
                 auxiliary options.
        reg: A Regexp object that holds all regexps that will be used in spec-cleaner.
        section_starts: A list of tuples where the first item is regex object
                       representing a start of the specfile section and the second is
                       a corresponding class that should handle it.
        _previous_line: A string holding the previous line of the currently processed
                        specfile.
        _previous_nonempty_line: A string holding a nonempty previous line of the
                                 currently processed specfile.
    """

    specfile: Optional[str] = None
    current_section: Section
    skip_run: bool = False
    _previous_line: Optional[str] = None
    _previous_nonempty_line: Optional[str] = None

    def __init__(self, options: Dict[str, Any]) -> None:
        """Initialize and load options into the RpmSpecCleaner obj and run prep methods.

        Args:
            options: A dictionary holding spec-cleaner command line options.
        """
        self.options = options

        # Initialize main license and subpkg option
        self.options['license'] = None
        self.options['subpkglicense'] = False

        # Compile keywords for unbracing
        self.options['unbrace_keywords'] = self._unbrace_keywords()

        # Load all the remaining file operations
        self.options['tex_conversions'] = []
        self.options['pkgconfig_conversions'] = []
        self.options['cmake_conversions'] = []
        self.options['perl_conversions'] = []
        if self.options['tex']:
            self.options['tex_conversions'] = read_tex_changes()
        if self.options['pkgconfig']:
            self.options['pkgconfig_conversions'] = read_pkgconfig_changes()
        if self.options['cmake']:
            self.options['cmake_conversions'] = read_cmake_changes()
        if self.options['perl']:
            self.options['perl_conversions'] = read_perl_changes()
        self.options['license_conversions'] = read_licenses_changes()
        if self.options['remove_groups']:
            self.options['allowed_groups'] = None
        else:
            self.options['allowed_groups'] = read_group_changes()
        self.options['reg'] = Regexp(self.options['unbrace_keywords'])

        # If gvim is used for the diff then run it in foreground mode
        if self.options['diff_prog'].startswith('gvim') and ' -f' not in self.options['diff_prog']:
            self.options['diff_prog'] += ' -f'

        self.reg = self.options['reg']
        self.fin = open_stringio_spec(self.options['specfile'])

        # Section starts detection
        self.section_starts = [
            (self.reg.re_spec_package, RpmPackage),
            (self.reg.re_spec_description, RpmDescription),
            (self.reg.re_spec_prep, RpmPrep),
            (self.reg.re_spec_build, RpmBuild),
            (self.reg.re_spec_install, RpmInstall),
            (self.reg.re_spec_clean, RpmClean),
            (self.reg.re_spec_check, RpmCheck),
            (self.reg.re_spec_scriptlets, RpmScriptlets),
            (self.reg.re_spec_triggers, RpmScriptlets),
            (self.reg.re_spec_files, RpmFiles),
            (self.reg.re_spec_changelog, RpmChangelog),
        ]

        # Find all the present licenses
        self._load_licenses()

        # Determine if we need to skip the spec ('#nospeccleaner' tag)
        self._find_skip_parser()

        # Set what will be the output of the cleaning
        self._select_mode()

    def _select_mode(self) -> None:
        """
        Set up what will be the output of the cleaning process.

        Based on the options given to the commandline possible options are: output file, inline or a diff program
        showing differences.
        """
        self.fout: IO[Any]
        if self.options['output']:
            self.fout = open(self.options['output'], 'w')
        elif self.options['inline']:
            self.fout = open(self.options['specfile'], 'w')
        elif self.options['diff']:
            self.fout = tempfile.NamedTemporaryFile(
                mode='w+', prefix=os.path.split(self.options['specfile'])[-1] + '.', suffix='.spec',
            )
        else:
            self.fout = sys.stdout

    def _unbrace_keywords(self) -> List[str]:
        """
        Create a list of keywords that shouldn't be in the curly brackets.

        It searches for keywords in the whitelist file, global macro functions in 'rpm --showrc' and macro functions
        in the specfile.

        Returns:
            A list of such keywords.
        """
        keywords = load_keywords_whitelist()
        global_macrofuncs = parse_rpm_showrc()
        spec_macrofuncs = find_macros_with_arg(self.options['specfile'])
        return keywords + global_macrofuncs + spec_macrofuncs

    def _find_skip_parser(self) -> None:
        """
        Search the specfile for the user defined '#nospeccleaner' tag.

        This tag means that specfile shouldn't be cleaned. If the tag is found then
        skip_run member is set to True, else it's False.
        """
        for line in self.fin:
            if self.reg.re_skipcleaner.match(line):
                self.skip_run = True
                break
        self.fin.seek(0)

    def _load_licenses(self) -> None:
        """
        Detect all present licenses in the specfile and load them into 'options' member.

        If we have more than one then put license to the each subpkg.
        """
        licenses: List[str] = []
        for line in self.fin:
            if self.reg.re_license.match(line):
                line = line.rstrip('\n')
                line = line.rstrip('\r')
                line = line.rstrip()
                match = self.reg.re_license.match(line)
                value = match.groups()[-1]
                if value not in licenses:
                    licenses.append(value)
        if len(licenses) > 1:
            self.options['subpkglicense'] = True
            # put first license as placeholder if main preamble is missing one
            self.options['license'] = licenses[0]
        self.fin.seek(0)

    def _detect_preamble_section(self, line: str) -> bool:
        """
        Detect if the line starts a preamble or not.

        Args:
            line: A string representing a line to process.

        Returns:
            True if it's a preamble, False otherwise.
        """
        # This is seriously ugly but can't think of cleaner way FIXME
        if not isinstance(self.current_section, (RpmPreamble, RpmPackage)):
            if any(re.match(line) for re in [self.reg.re_bcond_with, self.reg.re_debugpkg]):
                return True

            # We can have locally defined variables in phases
            if not isinstance(self.current_section, (RpmInstall, RpmCheck, RpmBuild, RpmPrep)) and (
                self.reg.re_define.match(line) or self.reg.re_global.match(line)
            ):
                return True
        return False

    def _detect_condition_change(self, line: str) -> bool:
        """
        Detect if the line contains a condition change.

        (e.g. '%endif', '%else' or the end of the code block)

        Args:
            line: A string representing a line to process.

        Returns:
             True if a condition change was found, False otherwise.
        """
        if any(
            re.match(line)
            for re in [self.reg.re_endif, self.reg.re_else_elif, self.reg.re_endcodeblock]
        ):
            return True
        return False

    def _detect_new_section(self, line: str) -> Optional[Type[Section]]:
        """
        Detect if the line contains a new section (and which) or not.

        Args:
            line: A string representing a line to process.

        Returns:
            A Section (or a subclass) object that was detected.
            None if we are staying in the same section or if we have a multiline value from preamble.
        """
        # Detect if we have multiline value from preamble
        # mypy: we need to ignore type check here because mypy cannot detect that we are checking the existence of
        # the 'multiline' attribute before accessing it
        if hasattr(self.current_section, 'multiline') and self.current_section.multiline:  # type: ignore
            return None

        # Detect if we match condition and that is from global space
        # Ie like in the optional packages where if is before class definition
        # For the "if" we need to detect it more smartly:
        #   check if the current line is starting new section, and if so
        #   if previous non-empty-uncommented line was starting the condition
        # we end up the condition section in preamble (if applicable) and
        # proceed to output
        if self._detect_condition_change(line) or (
            type(self.current_section) is Section
            and (self.reg.re_if.match(line) or self.reg.re_codeblock.match(line))
        ):
            if not hasattr(self.current_section, 'condition') or (
                hasattr(self.current_section, 'condition') and not self.current_section.condition
            ):
                # If we have to break out we go ahead with small class
                # which just print the one evil line
                return Section

        # try to verify if we start some specific section
        for (regexp, newclass) in self.section_starts:
            if regexp.match(line):
                # check if we are in if conditional and act accordingly if we
                # change sections
                if hasattr(self.current_section, 'condition') and self.current_section.condition:
                    self.current_section.condition = False
                    if hasattr(self.current_section, 'end_subparagraph'):
                        # mypy: we need to ignore type check here because mypy cannot detect that we are checking the
                        # existence of the 'end_subparagraph' attribute before accessing it
                        self.current_section.end_subparagraph(True)  # type: ignore
                return newclass

        # if we still are here and we are just doing copyright
        # and we are not on commented line anymore, just jump to Preamble
        if isinstance(self.current_section, RpmCopyright):
            if not self.reg.re_comment.match(line):
                return RpmPreamble
            # if we got two empty lines then the copyright also ended
            if self._previous_line == '' and line == '':
                self.current_section.add(line)
                return RpmPreamble

        # If we actually start matching global content again we need to
        # switch back to preamble, ie %define after %description/etc.
        if self._detect_preamble_section(line):
            return RpmPreamble

        # If we are in clean section and encounter whitespace
        # we need to stop deleting
        # This avoids deleting %if before %files section
        if isinstance(self.current_section, RpmClean) and line.strip() == '':
            return Section

        # we are staying in the section
        return None

    def _check_for_newline(self, detected_class: Optional[Type[Section]], line: str) -> bool:
        """
        Check if we want newline or not after the end of section detected.

        Args:
            detected_class: A Section class (or a subclass) representing section that needs to be checked.
            line: A string representing a line to process.

        Returns: True if we want a newline, False otherwise.
        """
        # We don't want to print newlines before %else and %endif
        if detected_class == Section and self._detect_condition_change(line):
            return False
        else:
            # We also do not want to print newline if at the end of the
            # previous section we actually had a commentary, ie comment above
            # new section
            if self._previous_line and self._previous_line.startswith('#'):
                return False
            else:
                return True

    def run(self) -> None:
        """
        Run the main spec-cleaner method.

        Raises:
            RpmExceptionError if a diff program can't be executed.
        """
        # If we are skipping the specfile we should do nothing
        if self.skip_run:
            sys.stderr.write(
                ".spec file {0} is not being processed due to definiton of 'nospeccleaner'\n".format(
                    self.options['specfile']
                )
            )
            for line in self.fin:
                self.fout.write(line)
            self.fout.flush()
            return

        # We always start with Copyright
        self.current_section = RpmCopyright(self.options)

        # FIXME: we need to store the content locally and then reorder
        #        to maintain the specs all the same (eg somebody put
        #        filelist to the top).
        for line in self.fin:
            # Remove newlines to make it easier to parse things
            line = line.rstrip('\n')
            line = line.rstrip('\r')

            new_class = self._detect_new_section(line)
            # Following line is debug output with class info
            # USE: 'spec-cleaner file > /dev/null' to see the stderr output
            # sys.stderr.write("class: '{0}' line: '{1}'\n".format(new_class, line))
            if new_class:
                self.current_section.output(
                    self.fout, self._check_for_newline(new_class, line), new_class.__name__,
                )
                # start new class
                self.current_section = new_class(self.options)
                # skip empty line adding if we are switching sections
                if self._previous_line == '' and line == '':
                    continue

            # Do not store data from clean and skip out here
            if isinstance(self.current_section, RpmClean):
                continue

            self.current_section.add(line)
            self._previous_line = line
            if line != '' and not line.startswith('#'):
                self._previous_nonempty_line = line

        # no need to not output newline at the end even for minimal -> no condition
        self.current_section.output(self.fout)
        # add changelog at the end of the file
        if (
            not isinstance(self.current_section, RpmChangelog)
            and self._previous_nonempty_line != '%changelog'
        ):
            self.fout.write('%changelog\n')
        self.fout.flush()

        # if the '--diff' option was used, run the diff program
        if self.options['diff']:
            cmd = shlex.split(
                self.options['diff_prog']
                + ' '
                + self.options['specfile'].replace(' ', '\\ ')
                + ' '
                + self.fout.name.replace(' ', '\\ ')
            )
            try:
                subprocess.call(cmd, shell=False)
            except OSError as error:
                raise RpmExceptionError(
                    'Could not execute %s (%s)'
                    % (self.options['diff_prog'].split()[0], error.strerror)
                )

    def __del__(self) -> None:
        """Close the input and output files."""
        if self.fin:
            self.fin.close()
        if self.fout:
            self.fout.close()
