# vim: set ts=4 sw=4 et: coding=UTF-8


class Section(object):
    """
    Basic object for parsing each section of spec file.
    It stores the lines in a list and remembers content of
    previous line at hand.
    """

    def __init__(self):
        self.lines = []
        self.previous_line = None

    def add(self, line):
        line = line.rstrip()
        line = replace_all(line)
        self.lines.append(line)
        self.previous_line = line

    def output(self, fout):
        for line in self.lines:
            fout.write(line + '\n')
