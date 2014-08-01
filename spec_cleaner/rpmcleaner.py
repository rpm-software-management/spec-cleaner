# vim: set ts=4 sw=4 et: coding=UTF-8

import io
import sys
import tempfile
import subprocess
import shlex
import os.path

from rpmsection import Section
from rpmexception import RpmException
from rpmcopyright import RpmCopyright
from rpmdescription import RpmDescription
from rpmprune import RpmClean
from rpmprune import RpmChangelog
from rpmpreamble import RpmPreamble
from rpmpreamble import RpmPackage
from rpmprep import RpmPrep
from rpmbuild import RpmBuild
from rpmcheck import RpmCheck
from rpminstall import RpmInstall
from rpmscriplets import RpmScriptlets
from rpmfiles import RpmFiles
from rpmregexp import RegexpSingle


class RpmSpecCleaner:
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


    def __init__(self, specfile, output, pkgconfig, inline, diff, diff_prog):
        self.specfile = specfile
        self.output = output
        self.pkgconfig = pkgconfig
        self.inline = inline
        self.diff = diff
        self.diff_prog = diff_prog
        #run gvim(diff) in foreground mode
        if self.diff_prog.startswith("gvim") and not " -f" in self.diff_prog:
            self.diff_prog += " -f"
        self.reg = RegexpSingle(specfile)
        self.fin = open(self.specfile)

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

        if self.output:
            self.fout = open(self.output, 'w')
        elif self.inline:
            fifo = io.BytesIO()
            while True:
                bytes = self.fin.read(500 * 1024)
                if len(bytes) == 0:
                    break
                fifo.write(bytes)

            self.fin.close()
            fifo.seek(0)
            self.fin = fifo
            self.fout = open(self.specfile, 'w')
        elif self.diff:
            self.fout = tempfile.NamedTemporaryFile(prefix=os.path.split(self.specfile)[-1]+'.', suffix='.spec')
        else:
            self.fout = sys.stdout


    def _detect_new_section(self, line):
        # Detect if we have multiline value from preamble
        if hasattr(self.current_section, 'multiline') and self.current_section.multiline:
            return None

        # Detect if we match condition and that is from global space
        # Ie like in the optional packages where if is before class definition
        # For the "if" we need to detect it more smartly:
        #   check if the current line is starting new section, and if so
        #   if previous non-empty-uncommented line was starting the condition
        #   we end up the condition section in preamble (if applicable) and proceed to output
        if self.reg.re_else.match(line) or self.reg.re_endif.match(line):
            if hasattr(self.current_section, 'condition') and not self.current_section.condition:
                # If we have to break out we go ahead with small class
                # which just print the one evil line
                return Section

        # try to verify if we start some specific section
        for (regexp, newclass) in self.section_starts:
            if regexp.match(line):
                # check if we are in if conditional and act accordingly if we change sections
                if self._previous_nonempty_line and self.reg.re_if.match(self._previous_nonempty_line):
                    if hasattr(self.current_section, 'condition'):
                        self.current_section.condition = False
                        self.current_section._end_subparagraph(True)
                return newclass

        # if we still are here and we are just doing copyright
        # and we are not on commented line anymore, just jump to Preamble
        if isinstance(self.current_section, RpmCopyright):
            if not self.reg.re_comment.match(line):
                return RpmPreamble
            # if we got two whitespaces then the copyright also ended
            if self._previous_line == '' and line == '':
                return RpmPreamble

        # If we are in clean section and encounter whitespace
        # we need to stop deleting
        # This avoids deleting %if before %files section that could
        # be deleted otherwise
        if isinstance(self.current_section, RpmClean):
           if line.strip() == '':
               return Section

        # we are staying in the section
        return None


    def run(self):
        # We always start with Copyright
        self.current_section = RpmCopyright(self.specfile)

        # FIXME: we need to store the content localy and then reorder
        #        to maintain the specs all the same (eg somebody put
        #        filelist to the top).
        for line in self.fin:
            # Stop at the end of the file
            if len(line) == 0:
                break
            # Remove \n to make it easier to parse things
            line = line.rstrip('\n')
            line = line.rstrip('\r')

            new_class = self._detect_new_section(line)
            #sys.stderr.write("class: '{0}' line: '{1}'\n".format(new_class, line))
            if new_class:
                self.current_section.output(self.fout)
                # we need to sent pkgconfig option to preamble and package
                if new_class == RpmPreamble or new_class == RpmPackage:
                    self.current_section = new_class(self.specfile, self.pkgconfig)
                else:
                    self.current_section = new_class(self.specfile)
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

        self.current_section.output(self.fout)
        self.fout.flush()

        if self.diff:
            cmd = shlex.split(self.diff_prog + " " + self.specfile.replace(" ","\\ ") + " " + self.fout.name.replace(" ","\\ "))
            try:
                subprocess.call(cmd, shell=False)
            except OSError as e:
                raise RpmException('Could not execute %s (%s)' % (self.diff_prog.split()[0], e.strerror))


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
