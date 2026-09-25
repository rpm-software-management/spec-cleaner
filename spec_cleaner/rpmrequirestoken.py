from .rpmexception import RpmExceptionError
from .rpmregexp import Regexp


class RpmRequiresToken:
    """
    Class containing information about the dependency token.

    Process dependencies like Requires, Recommends, Suggests, Supplements, Enhances, Conflicts. Can be used to specify
    all the values present on the line. Later on we use this to do various conversions.

    This class uses the following format and naming:

    prefix            name          operator   version
    BuildRequires:    boringpackage >=         5.2.8
    """

    comments: str | None = None
    trailing_comment: str | None = None

    def __init__(
        self,
        name: str,
        operator: str | None = None,
        version: str | None = None,
        prefix: str | None = None,
    ) -> None:
        """Initialize class."""
        self.prefix = prefix
        self.name = name
        self.operator = operator
        self.version = version

    @staticmethod
    def _format_operator(operator: str) -> str:
        """
        Make sure the operators look sane and not use all permutations.

        Args:
            operator: A string representing the operator used in the dependency token.

        Returns:
            Formatted operator.
        """
        operator = operator.replace('=<', '<=')
        operator = operator.replace('=>', '>=')
        operator = operator.replace('==', '=')
        return operator

    @staticmethod
    def _format_name(name: str) -> str:
        """
        Make sure the name looks sane and make various replacements.

        Args:
            name: A string representing the name used in the dependency token.

        Returns:
            Formatted name.
        """
        # we just rename pkgconfig names to one unified one working everywhere
        if name == 'pkgconfig(pkg-config)' or name == 'pkg-config':
            name = 'pkgconfig'

        # omit legacy 'otherproviders' codeblock
        match = Regexp.re_otherproviders.match(name)
        if match:
            name = match.group(1)

        # replace 'packageand(pkgA:pkgB)' with '(pkgA and pkgB)' - new in RPM 4.13
        match = Regexp.re_packageand.match(name)
        if match:
            name = f'({match.group(1)} and {match.group(2)})'
            # macros inside packageand() are shielded from brace expansion by
            # the ':' separator, so brace them here to keep the output stable
            previous = None
            while name != previous:
                previous = name
                name = Regexp.re_macro.sub(r'\1%{\3}\5', name)
        return name

    def __str__(self) -> str:
        """
        Output it all on nice pretty line.

        Returns:
            A string with a formatted output.

        Raises:
            RpmExceptionError if prefix or name is not defined or the version is defined but no operator is present.
        """
        self.name = self._format_name(self.name)
        if not self.prefix:
            raise RpmExceptionError(
                f'No defined prefix in RequiresToken: prefix "{self.prefix}" name "{self.name}" operator "{self.operator}" version "{self.version}"'
            )
        if not self.name:
            raise RpmExceptionError(
                f'No defined name in RequiresToken: prefix "{self.prefix}" name "{self.name}" operator "{self.operator}" version "{self.version}"'
            )
        string = self.prefix + self.name
        if (self.version and not self.operator) or (not self.version and self.operator):
            raise RpmExceptionError('Have defined version and no operator or vice versa')
        if self.version and self.operator:
            self.operator = self._format_operator(self.operator)
            string += ' ' + self.operator + ' ' + self.version
        if self.trailing_comment:
            string += ' ' + self.trailing_comment

        return string
