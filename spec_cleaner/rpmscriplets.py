# vim: set ts=4 sw=4 et: coding=UTF-8

from rpmsection import Section


class RpmScriptlets(Section):
    '''
        Do %post -p /sbin/ldconfig when possible.
    '''


    def __init__(self, specfile):
        Section.__init__(self, specfile)
        self.cache = []


    def add(self, line):
        if len(self.lines) == 0:
            if not self.cache:
                if line.find(' -p ') == -1 and line.find(' -f ') == -1:
                    self.cache.append(line)
                    return
            else:
                if line in ['', '/sbin/ldconfig' ]:
                    self.cache.append(line)
                    return
                else:
                    for cached in self.cache:
                        Section.add(self, cached)
                    self.cache = None

        Section.add(self, line)


    def output(self, fout):
        if self.cache:
            Section.add(self, self.cache[0] + ' -p /sbin/ldconfig')
            Section.add(self, '')

        Section.output(self, fout)
