# vim: set ts=4 sw=4 et: coding=UTF-8

import os
import sys
import cStringIO
import optparse
import re
import time
import tempfile
import subprocess
import shlex

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
from rpminstall import RpmInstall
from rpmscriplets import RpmScriptlets
from rpmfiles import RpmFiles
from fileutils import FileUtils

BRACKETING_EXCLUDES = 'excludes-bracketing.txt'

re_comment = re.compile('^$|^\s*#')

class RpmSpecCleaner:
    specfile = None
    fin = None
    fout = None
    current_section = None

    re_spec_package = re.compile('^%package\s*', re.IGNORECASE)
    re_spec_description = re.compile('^%description\s*', re.IGNORECASE)
    re_spec_prep = re.compile('^%prep\s*$', re.IGNORECASE)
    re_spec_build = re.compile('^%build\s*$', re.IGNORECASE)
    re_spec_install = re.compile('^%install\s*$', re.IGNORECASE)
    re_spec_clean = re.compile('^%clean\s*$', re.IGNORECASE)
    re_spec_scriptlets = re.compile('(?:^%pretrans\s*)|(?:^%pre\s*)|(?:^%post\s*)|(?:^%preun\s*)|(?:^%postun\s*)|(?:^%posttrans\s*)', re.IGNORECASE)
    re_spec_files = re.compile('^%files\s*', re.IGNORECASE)
    re_spec_changelog = re.compile('^%changelog\s*$', re.IGNORECASE)

    re_spec_macrofunc = re.compile(r'^\s*%define\s(\w+)\(.*')

    section_starts = [
        (re_spec_package, RpmPackage),
        (re_spec_description, RpmDescription),
        (re_spec_prep, RpmPrep),
        (re_spec_build, RpmBuild),
        (re_spec_install, RpmInstall),
        (re_spec_clean, RpmClean),
        (re_spec_scriptlets, RpmScriptlets),
        (re_spec_files, RpmFiles),
        (re_spec_changelog, RpmChangelog)
    ]


    def __init__(self, specfile, output, inline, diff, diff_prog):
        self.specfile = specfile
        self.output = output
        self.inline = inline
        self.diff = diff
        self.diff_prog = diff_prog

        global global_macrofuncs
        global_macrofuncs = self.parse_rpm_showrc()
        glob_macrofuncs = global_macrofuncs

        spec_macrofuncs = self.find_macros_with_arg(specfile)

        files = FileUtils()
        f = files.open_datafile(BRACKETING_EXCLUDES)

        keywords= []
        for line in f:
            keywords.append(line[:-1])

        self.re_unbrace_keywords = re.compile('%{(' + '|'.join(keywords + glob_macrofuncs + spec_macrofuncs) + ')}')

        self.fin = open(self.specfile)

        if self.output:
            self.fout = open(self.output, 'w')
        elif self.inline:
            io = cStringIO.StringIO()
            while True:
                bytes = self.fin.read(500 * 1024)
                if len(bytes) == 0:
                    break
                io.write(bytes)

            self.fin.close()
            io.seek(0)
            self.fin = io
            self.fout = open(self.specfile, 'w')
        elif self.diff:
            self.fout = tempfile.NamedTemporaryFile(prefix=self.specfile+'.', suffix='.spec')
        else:
            self.fout = sys.stdout

    def parse_rpm_showrc(self):
        macros = []
        re_rc_macrofunc = re.compile(r'^-[0-9]+[:=]\s(\w+)\(.*')
        output = os.popen('rpm --showrc')
        for line in output.readlines():
            line = line[:-1]
            found_macro = re_rc_macrofunc.sub(r'\1', line)
            if found_macro != line:
                macros += [ found_macro ]
        output.close()
        return macros

    def run(self):
        def _line_for_new_section(self, line):
            if isinstance(self.current_section, RpmCopyright):
                if not re_comment.match(line):
                    return RpmPreamble

            for (regexp, newclass) in self.section_starts:
                if regexp.match(line):
                    return newclass

            return None


        self.current_section = RpmCopyright(self.re_unbrace_keywords, self.specfile)

        while True:
            line = self.fin.readline()
            if len(line) == 0:
                break
            # Remove \n to make it easier to parse things
            line = line[:-1]

            new_class = _line_for_new_section(self, line)
            if new_class:
                self.current_section.output(self.fout)
                self.current_section = new_class(self.re_unbrace_keywords)

            self.current_section.add(line)

        self.current_section.output(self.fout)
        self.fout.flush()

        if self.diff:
            cmd = shlex.split(self.diff_prog + " " + self.specfile.replace(" ","\\ ") + " " + self.fout.name.replace(" ","\\ "))
            try:
                subprocess.call(cmd, shell=False)
            except OSError as e:
                raise RpmException('Could not execute %s (%s)' % (self.diff_prog.split()[0], e.strerror))

    def find_macros_with_arg(self, spec):
        macrofuncs = []
        specfile = open(spec, 'r')
        for line in specfile.readlines():
            line = line[:-1]
            found_macro = self.re_spec_macrofunc.sub(r'\1', line)
            if found_macro != line:
                macrofuncs += [ found_macro ]
        specfile.close()
        return macrofuncs

    def __del__(self):
        if self.fin:
            self.fin.close()
            self.fin = None
        if self.fout:
            self.fout.close()
            self.fout = None
