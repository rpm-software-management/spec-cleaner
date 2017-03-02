# vim: set ts=4 sw=4 et: coding=UTF-8

import getopt
import shlex
import re
import os

from .rpmsection import Section


class RpmFiles(Section):

    """
        Class that does replacements on the %files section.
    """

    re_alternative = re.compile(r'^%ghost %\{_sysconfdir\}/alternatives/(.*)$')

    comment_present = False

    def __init__(self, options):
        Section.__init__(self, options)
        self.kill_alternatives = set()

    def add(self, line):
        if len(self.lines) == 0:
            line = self._ensure_python_files(line)

        line = self._complete_cleanup(line)
        line = self.strip_useless_spaces(line)
        line = self._remove_doc_on_man(line)

        if not self.minimal:
            self._add_defattr(line)
            line = self._set_man_compression(line)

        if line.startswith("%{_bindir}"):
            line = "%python3_only " + line
        if line.endswith(".py*") or line.endswith(".pyc"):
            pycachepath = os.path.join(os.path.dirname(line), "__pycache__/*")
            Section.add(self, "%pycache_only " + pycachepath)

        alt = self.re_alternative.match(line)
        if alt:
            self.kill_alternatives.add(alt.group(1))
            return

        # toss out empty lines if there are more than one in succession
        if line == '' and (not self.previous_line or self.previous_line == ''):
            return

        Section.add(self, line)

    def output(self, *args, **kwargs):
        for alternative in self.kill_alternatives:
            re_alt = re.compile(r'/' + alternative + r'-%\{python.?_version\}(\..*)?')
            self.lines = [l for l in self.lines if not re_alt.search(l)]

        Section.output(self, *args, **kwargs)

    def _ensure_python_files(self, line):
        if "%{python_files" in line:
            return line

        arglist = shlex.split(line)
        optlist, args = getopt.getopt(arglist[1:], 'f:n:')
        optdict = dict(optlist)
        if "-n" in optdict:
            return line

        newline = ["%files"]
        for k,v in optlist:
            if " " in v:
                v = '"' + v + '"'
            newline.append(k)
            newline.append(v)
        if args:
            newline.append('%{python_files ' + args[0] + '}')
            newline += args[1:]
        else:
            newline.append('%{python_files}')
        return " ".join(newline)

    def _add_defattr(self, line):
        """
        Add defattr with default values if there is none
        Also be aware of comments that could've been put on top
        """
        if self.comment_present and not line.startswith('#'):
            self.comment_present = False
            if not line.startswith('%defattr'):
                self.lines.insert(1, '%defattr(-,root,root)')

        if self.previous_line and \
                self.reg.re_spec_files.match(self.previous_line):
            if line.startswith('#'):
                self.comment_present = True
            elif not line.startswith('%defattr'):
                self.lines.append('%defattr(-,root,root)')

    def _remove_doc_on_man(self, line):
        """
        Remove all %doc %_mandir to -> %_mandir as it is pointless to do twice
        """
        line = line.replace("%doc %{_mandir}", "%{_mandir}", 1)
        line = line.replace("%doc %{_infodir}", "%{_infodir}", 1)
        return line

    def _set_man_compression(self, line):
        """
        Set proper compression suffix on man/info pages, instead of .gz/.* use
        the proper macro variable
        """
        if line.startswith("%{_mandir}"):
            line = self.reg.re_compression.sub('%{ext_man}', line)
        if line.startswith("%{_infodir}"):
            line = self.reg.re_compression.sub('%{ext_info}', line)
        return line
