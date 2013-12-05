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
        # firs try to verify if we start some specific section
        for (regexp, newclass) in self.section_starts:
            if regexp.match(line):
                return newclass

        # later if we still are here and we are just doing copyright
        # and we are not on commented line anymore, just jump to Preamble
        if isinstance(self.current_section, RpmCopyright):
            if not self.reg.re_comment.match(line):
                return RpmPreamble

        # we are staying in the section
        return None


    def run(self):
        # We always start with Copyright
        self.current_section = RpmCopyright(self.specfile)

        # FIXME: we need to store the content localy and then reorder
        #        to maintain the specs all the same (eg somebody put
        #        filelist to the top).
        while True:
            line = self.fin.readline()
            # Stop at the end of the file
            if len(line) == 0:
                break
            # Remove \n to make it easier to parse things
            line = line[:-1]

            new_class = self._detect_new_section(line)
            if new_class:
                self.current_section.output(self.fout)
                # we need to sent pkgconfig option to preamble and package
                if new_class == RpmPreamble or new_class == RpmPackage:
                    self.current_section = new_class(self.specfile, self.pkgconfig)
                else:
                    self.current_section = new_class(self.specfile)

            self.current_section.add(line)

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
