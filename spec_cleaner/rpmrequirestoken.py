from typing import Optional

from .rpmexception import RpmException


class RpmRequiresToken(object):
    """
    Class containing information about the dependency token.

    Can be used to specify all the values present on the line.
    Later on we use this to do various conversions.

    This class uses the following format and naming:

    prefix            name          operator   version
    BuildRequires:    boringpackage >=         5.2.8
    """

    name: Optional[str] = None
    operator: Optional[str] = None
    version: Optional[str] = None
    prefix: Optional[str] = None
    comments: Optional[str] = None

    def __init__(self, name: str, operator: Optional[str] = None, version: Optional[str] = None,
                 prefix: Optional[str] = None) -> None:
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
        Make sure the name looks sane.

        Args:
            name: A string representing the name used in the dependency token.

        Returns:
            Formatted name.
        """
        # we just rename pkgconfig names to one unified one working everywhere
        if name == 'pkgconfig(pkg-config)' or name == 'pkg-config':
            name = 'pkgconfig'
        # if there is otherproviders codeblock just ommit it
        if name.startswith('otherproviders('):
            name = name.rstrip(')')
            name = name.replace('otherproviders(', '')
        return name

    def __str__(self) -> str:
        """
        Output it all on nice pretty line.

        Returns:
            A string with a formatted output.

        Raises:
            RpmException if prefix or name is not defined or the version is defined but no operator is present.
        """

        self.name = self._format_name(self.name)
        if not self.prefix:
            raise RpmException(
                'No defined prefix in RequiresToken: prefix "{0}" name "{1}" operator "{2}" version "{3}"'.format(
                    self.prefix, self.name, self.operator, self.version
                )
            )
        if not self.name:
            raise RpmException(
                'No defined name in RequiresToken: prefix "{0}" name "{1}" operator "{2}" version "{3}"'.format(
                    self.prefix, self.name, self.operator, self.version
                )
            )
        string = self.prefix + self.name
        if self.version and not self.operator:
            raise RpmException('Have defined version and no operator %s' % self.version)
        if self.version:
            self.operator = self._format_operator(self.operator)
            string += ' ' + self.operator + ' ' + self.version

        return string
