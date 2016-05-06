# vim: set ts=4 sw=4 et: coding=UTF-8

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import sys
import tempfile
import subprocess
import shlex
import os.path

from .rpmsection import Section
from .rpmexception import RpmException
from .rpmcopyright import RpmCopyright
from .rpmdescription import RpmDescription
from .rpmprune import RpmClean
from .rpmprune import RpmChangelog
from .rpmpreamble import RpmPreamble
from .rpmpreamble import RpmPackage
from .rpmprep import RpmPrep
from .rpmbuild import RpmBuild
from .rpmcheck import RpmCheck
from .rpminstall import RpmInstall
from .rpmscriplets import RpmScriptlets
from .rpmfiles import RpmFiles
from .rpmregexp import RegexpSingle


class RpmSpecCleaner(object):

    """
    Class wrapping all section parsers reponsible for ensuring
    that all sections are checked and accounted for.
    If the section is required and not found it is created with
    blank values as fixme for the spec creator.
    """
    specfile = None
    fin = None
    fout = None
    current_section = None
    _previous_line = None
    _previous_nonempty_line = None

    def __init__(self, options):
        self.options = options
        # inicialize main license and subpkg option
        self.options['license'] = None
        self.options['subpkglicense'] = False
        # run gvim(diff) in foreground mode
        if self.options['diff_prog'].startswith("gvim") and " -f" not in self.options['diff_prog']:
            self.options['diff_prog'] += " -f"
        self.reg = RegexpSingle(self.options['specfile'])
        self.fin = open(self.options['specfile'])

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
            (self.reg.re_spec_files, RpmFiles),
            (self.reg.re_spec_changelog, RpmChangelog)
        ]

        self._load_licenses()

        if self.options['output']:
            self.fout = open(self.options['output'], 'w')
        elif self.options['inline']:
            fifo = StringIO()
            while True:
                string = self.fin.read(500 * 1024)
                if len(string) == 0:
                    break
                fifo.write(string)

            self.fin.close()
            fifo.seek(0)
            self.fin = fifo
            self.fout = open(self.options['specfile'], 'w')
        elif self.options['diff']:
            self.fout = tempfile.NamedTemporaryFile(mode='w+', prefix=os.path.split(self.options['specfile'])[-1] + '.', suffix='.spec')
        else:
            self.fout = sys.stdout

    def _load_licenses(self):
        # detect all present licenses in the spec and detect if we have more
        # than one. If we do put license to each subpkg
        licenses = []
        filecontent = open(self.options['specfile'])
        for line in filecontent:
            if self.reg.re_license.match(line):
                line = line.rstrip('\n')
                line = line.rstrip('\r')
                line = line.rstrip()
                match = self.reg.re_license.match(line)
                value = match.groups()[len(match.groups()) - 1]
                if value not in licenses:
                    licenses.append(value)
        filecontent.close()
        filecontent = None
        if len(licenses) > 1:
            self.options['subpkglicense'] = True
            # put first license as placeholder if main preamble is missing one
            self.options['license'] = licenses[0]

    def _detect_preamble_section(self, line):
        # This is seriously ugly but can't think of cleaner way
        # WARN: Keep in sync with rpmregexps for rpmpreamble section
        if not isinstance(self.current_section, (RpmPreamble, RpmPackage)):
            if any([re.match(line) for re in [
                   self.reg.re_bcond_with, self.reg.re_requires,
                   self.reg.re_requires_phase, self.reg.re_buildrequires,
                   self.reg.re_prereq, self.reg.re_recommends,
                   self.reg.re_suggests, self.reg.re_name,
                   self.reg.re_version, self.reg.re_release,
                   self.reg.re_license, self.reg.re_summary,
                   self.reg.re_summary_localized, self.reg.re_url,
                   self.reg.re_group, self.reg.re_vendor,
                   self.reg.re_source, self.reg.re_patch,
                   self.reg.re_enhances, self.reg.re_supplements,
                   self.reg.re_conflicts, self.reg.re_provides,
                   self.reg.re_obsoletes, self.reg.re_buildroot,
                   self.reg.re_buildarch, self.reg.re_epoch,
                   self.reg.re_icon, self.reg.re_packager,
                   self.reg.re_debugpkg, self.reg.re_requires_eq,
                   self.reg.re_preamble_prefix,
               ]]):
                return True

            # We can have locally defined variables in phases
            if not isinstance(self.current_section,
                   (RpmInstall, RpmCheck, RpmBuild, RpmPrep)) and \
               (self.reg.re_define.match(line) or self.reg.re_global.match(line)):
                return True
        return False

    def _detect_new_section(self, line):
        # Detect if we have multiline value from preamble
        if hasattr(self.current_section, 'multiline') and self.current_section.multiline:
            return None

        # Detect if we match condition and that is from global space
        # Ie like in the optional packages where if is before class definition
        # For the "if" we need to detect it more smartly:
        #   check if the current line is starting new section, and if so
        #   if previous non-empty-uncommented line was starting the condition
        # we end up the condition section in preamble (if applicable) and
        # proceed to output
        if self.reg.re_else.match(line) or self.reg.re_endif.match(line) or \
           (type(self.current_section) is Section and self.reg.re_if.match(line)):
            if not hasattr(self.current_section, 'condition') or \
               (hasattr(self.current_section, 'condition') and not self.current_section.condition):
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
                        self.current_section.end_subparagraph(True)
                return newclass

        # if we still are here and we are just doing copyright
        # and we are not on commented line anymore, just jump to Preamble
        if isinstance(self.current_section, RpmCopyright):
            if not self.reg.re_comment.match(line):
                return RpmPreamble
            # if we got two whitespaces then the copyright also ended
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

    def run(self):
        # We always start with Copyright
        self.current_section = RpmCopyright(self.options)

        # FIXME: we need to store the content localy and then reorder
        #        to maintain the specs all the same (eg somebody put
        #        filelist to the top).
        line = None
        for line in self.fin:
            # Remove \n to make it easier to parse things
            line = line.rstrip('\n')
            line = line.rstrip('\r')

            new_class = self._detect_new_section(line)
            # Following line is debug output with class info
            # USE: 'spec-cleaner file > /dev/null' to see the stderr output
            #sys.stderr.write("class: '{0}' line: '{1}'\n".format(new_class, line))
            if new_class:
                # We don't want to print newlines before %else and %endif
                if new_class == Section and (self.reg.re_else.match(line) or self.reg.re_endif.match(line)):
                    newline = False
                else:
                    newline = True
                self.current_section.output(self.fout, newline, new_class.__name__)
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
            if line != '' or not line.startswith('#'):
                self._previous_nonempty_line = line

        # no need to not output newline at the end even for minimal -> no condition
        self.current_section.output(self.fout)
        # add changelog at the end of the file
        if line is None or (line is not None and line != '%changelog'):
            self.fout.write('%changelog\n')
        self.fout.flush()

        if self.options['diff']:
            cmd = shlex.split(self.options['diff_prog'] + " " + self.options['specfile'].replace(" ", "\\ ") + " " + self.fout.name.replace(" ", "\\ "))
            try:
                subprocess.call(cmd, shell=False)
            except OSError as error:
                raise RpmException('Could not execute %s (%s)' % (self.options['diff_prog'].split()[0], error.strerror))

    def __del__(self):
        """
        We need to close the input and output files
        """

        if self.fin:
            self.fin.close()
            self.fin = None
        if self.fout:
            self.fout.close()
            self.fout = None
