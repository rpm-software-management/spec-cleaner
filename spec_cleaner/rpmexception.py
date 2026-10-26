# vim: set ts=4 sw=4 et: coding=UTF-8


class RpmBaseExceptionError(Exception):
    """Class wrapping Exception class so we throw neat exceptions."""

    def __init__(self, args: str | tuple[str, ...] = ()) -> None:
        """Initialise class."""
        super().__init__(*args)
        # callers pass a single message string, which is stored as-is;
        # typeshed types Exception.args as a tuple, hence the ignore
        self.args = args  # type: ignore[assignment]

    def __str__(self) -> str:
        """Format string representation."""
        return ''.join(self.args)


class RpmWrongArgsError(RpmBaseExceptionError):
    """Exception raised by wrong arguments passed by cli."""


class RpmExceptionError(RpmBaseExceptionError):
    """Exception raised by wrong parsed content from rpm."""


class NoMatchExceptionError(RpmBaseExceptionError):
    """Exception raised by not matching corresponding brackets/etc."""
