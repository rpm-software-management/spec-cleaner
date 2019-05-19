# vim: set ts=4 sw=4 et: coding=UTF-8


class RpmBaseException(Exception):

    """
    Class wrapping Exception class so we throw neat exceptions.
    """

    def __init__(self, args=()) -> None:
        Exception.__init__(self)
        self.args = args

    def __str__(self) -> str:
        return ''.join(self.args)


class RpmWrongArgs(RpmBaseException):

    """
    Exception raised by wrong arguments passed by cli.
    """


class RpmException(RpmBaseException):

    """
    Exception raised by wrong parsed content from rpm.
    """


class NoMatchException(RpmBaseException):

    """
    Exception raised by not matching corresponding brackets/etc.
    """
