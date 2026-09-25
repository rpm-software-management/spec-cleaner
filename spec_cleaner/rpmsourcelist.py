# vim: set ts=4 sw=4 et: coding=UTF-8

from .rpmsection import Section


class RpmSourceList(Section):
    """
    A class for the %sourcelist and %patchlist sections.

    It is kept apart from the plain Section, which only holds stray condition lines.
    """
