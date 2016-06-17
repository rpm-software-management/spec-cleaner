# vim: set ts=4 sw=4 et: coding=UTF-8


class Section(object):

    """
    Basic object for parsing each section of spec file.
    It stores the lines in a list and remembers content of
    previous line at hand.
    The unbrace_keywords content is passed from creating
    object to reduce calculation price.
    Various functions do replacement of common typos to
    unificate all the content.
    """

    def __init__(self, options):
        self.lines = []
        self.previous_line = None
        self.spec = options['specfile']
        self.minimal = options['minimal']
        self.reg = options['reg']
        # Are we inside of conditional or not
        self.condition = False
        self._condition_counter = 0

    def _complete_cleanup(self, line):
        """
        Function that just calls all the cleanups in proper order so it
        can be called beforehand if we override add phase and want to
        do our replaces after cleanup.
        """

        line = line.rstrip()

        if not line.startswith('#'):
            if not self.minimal:
                line = self.embrace_macros(line)
            line = self.replace_buildroot(line)
            line = self.replace_optflags(line)
            line = self.replace_known_dirs(line)
            line = self.replace_utils(line)
            line = self.replace_buildservice(line)
            line = self.replace_preamble_macros(line)

        return line

    def _check_conditions(self, line):
        """
        Check if we are in condition that is contained or not
        """
        if self.reg.re_if.match(line):
            self._condition_counter += 1
        if self.reg.re_endif.match(line):
            self._condition_counter -= 1

        if self._condition_counter > 0:
            self.condition = True
        else:
            self.condition = False

    def add(self, line):
        """
        Run the cleanup and add the line to the list of lines
        """

        line = self._complete_cleanup(line)

        # condtions detect
        self._check_conditions(line)

        # append to the file
        self.lines.append(line)
        self.previous_line = line

    def output(self, fout, newline=True, new_class=None):
        # Always append one empty line at the end if it is not present
        # and changelog is trailing part of our spec so do not put nothing
        # bellow
        # Also if we are jumping away just after writing one macroed line
        # we don't want to create new line
        if newline and len(self.lines) >= 1:
            if self.lines[-1] != '' and \
               self.lines[-1] != '%changelog' and not \
               self.lines[-1].startswith('%if') and not \
               self.lines[-1].startswith('%pre') and not \
               self.lines[-1].startswith('%post'):
                self.lines.append('')
            if new_class != 'RpmScriptlets' and \
               (self.lines[-1].startswith('%pre') or
                    self.lines[-1].startswith('%post')):
                self.lines.append('')
            # remove the newlines around ifs if they are not wanted
            if len(self.lines) >= 2:
                if self.lines[-1] == '' and \
                   (self.lines[-2].startswith('%if') or
                        self.lines[-2].startswith('%else')):
                    self.lines.pop()

        for line in self.lines:
            fout.write(line + '\n')

    def strip_useless_spaces(self, line):
        """
        Function to remove useless multiple spaces in some areas.
        It can't be called everywhere so we have to call it in
        children classes where fit.
        """
        return ' '.join(line.split())

    def embrace_macros(self, line):
        """
        Add {} around known macros that have no arguments and are not
        on whitelist.
        Whitelist is passed from caller object
        """

        # I don't think that this can be done within one regexp replacement
        # if you have idea, send me a patch :)

        # work only with non-commented part
        sp = line.split('#')
        # so, for now, put braces around everything, what looks like macro,
        previous = sp[0]

        while True:
            sp[0] = self.reg.re_macro.sub(r'\1%{\3}\5', sp[0])
            if sp[0] == previous:
                break
            else:
                previous = sp[0]

        # and replace back known keywords to braceless state again
        sp[0] = self.reg.re_unbrace_keywords.sub(r'%\1', sp[0])
        # re-create the line back
        return '#'.join(sp)

    def replace_buildroot(self, line):
        """
        Replace RPM_BUILD_ROOT for buildroot
        """
        line = self.reg.re_rpmbuildroot.sub(r'%{buildroot}\2', line)
        line = self.reg.re_rpmbuildroot_quotes.sub(r'%{buildroot}', line)
        return line

    def replace_optflags(self, line):
        """
        Replace RPM_OPT_FLAGS for %{optflags}
        """
        # if the optflags is the only thing then also add quotes around it
        line = self.reg.re_optflags_quotes.sub('="%{optflags}"', line)
        line = self.reg.re_optflags.sub('%{optflags}', line)
        return line

    def replace_known_dirs(self, line):
        """
        Replace hardcoded stuff like /usr/share -> %{_datadir}
        """

        line = self.reg.re_oldprefix.sub(r'%{_prefix}\1', line)
        line = self.reg.re_prefix.sub(r'%{_prefix}\1', line)
        line = self.reg.re_bindir.sub(r'%{_bindir}\1', line)
        line = self.reg.re_sbindir.sub(r'%{_sbindir}\1', line)
        # Disabled on purpose as it causes conflict in fedora/opensuse
        # Unfortunate but there is no reliable workaround
        # line = self.reg.re_libexecdir.sub(r'%{_libexecdir}\1', line)
        line = self.reg.re_includedir.sub(r'%{_includedir}\1', line)
        line = self.reg.re_datadir.sub(r'%{_datadir}\1', line)
        line = self.reg.re_mandir.sub(r'%{_mandir}\1', line)
        line = self.reg.re_infodir.sub(r'%{_infodir}\1', line)
        line = self.reg.re_docdir.sub(r'%{_docdir}\1', line)
        line = self.reg.re_initdir.sub(r'%{_initddir}\1', line)
        line = self.reg.re_sysconfdir.sub(r'%{_sysconfdir}\1', line)
        line = self.reg.re_localstatedir.sub(r'%{_localstatedir}\1', line)
        line = self.reg.re_libdir.sub(r'%{_libdir}\2', line)
        line = self.reg.re_initddir.sub(r'%{_initddir}\1', line)

        return line

    def replace_utils(self, line):
        """
        Remove the macro calls for utilities and rather use direct commands.
        OBS ensures there is only one anyway.
        """
        r = {'id_u': 'id -u', 'ln_s': 'ln -s', 'lzma': 'xz --format-lzma', 'mkdir_p': 'mkdir -p',
             'awk': 'gawk', 'cc': 'gcc', 'cpp': 'gcc -E', 'cxx': 'g++', 'remsh': 'rsh', }
        for i in r:
            line = line.replace('%{__' + i + '}', r[i])
            if self.minimal:
                line = line.replace('%__' + i, r[i])

        for i in ['aclocal', 'ar', 'as', 'autoconf', 'autoheader', 'automake', 'bzip2', 'cat', 'chgrp', 'chmod', 'chown', 'cp', 'cpio', 'file', 'gpg', 'grep', 'gzip', 'id', 'install', 'ld', 'libtoolize', 'make', 'mkdir', 'mv', 'nm', 'objcopy', 'objdump', 'patch', 'perl', 'python', 'ranlib', 'restorecon', 'rm', 'rsh', 'sed', 'semodule', 'ssh', 'strip', 'tar', 'unzip', 'xz']:
            line = line.replace('%{__' + i + '}', i)
            if self.minimal:
                line = line.replace('%__' + i, i)

        return line

    def replace_buildservice(self, line):
        """
        Pretty format the conditions for distribution/version detection.
        Replace %{suse_version} for 0%{?suse_version}
        """
        for i in ['centos', 'debian', 'fedora', 'mandriva', 'meego', 'rhel', 'sles', 'suse', 'ubuntu']:
            line = line.replace('%{' + i + '_version}', '0%{?' + i + '_version}').replace('00%{', '0%{')
        return line

    def replace_preamble_macros(self, line):
        """
        Replace %{S:0} for %{SOURCE0} and so on.
        """
        line = self.reg.re_ptch.sub(r'%{PATCH\1}', line)
        line = self.reg.re_src.sub(r'%{SOURCE\1}', line)
        return line
