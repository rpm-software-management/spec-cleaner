from .rpmexception import RpmException

class RpmRequiresToken(object):
    """
    Class containing informations about the dependency token
    Can be used to specify all the values present on the line
    Later on we use this to do various conversions

    prefix            name          operator   version
    BuildRequires:    boringpackage >=         5.2.8
    """

    name = None
    operator = None
    version = None
    prefix = None
    comments = None

    def __init__(self, name, operator = None, version = None, prefix = None):
        self.prefix = prefix
        self.name = name
        self.operator = operator
        self.version = version

    def _format_operator(self, operator):
        """
        Make sure the operators look sane and not use all permutations
        """
        operator = operator.replace('=<', '<=')
        operator = operator.replace('=>', '>=')
        return operator

    def _format_name(self, name):
        # we just rename pkgconfig names to one unified one working everywhere
        if name == 'pkgconfig(pkg-config)' or name == 'pkg-config':
            name = 'pkgconfig'
        return name

    def __str__(self):
        """
        Output it all on nice pretty line
        """

        self.name = self._format_name(self.name)
        if not self.prefix:
            raise RpmException('No defined prefix in RequiresToken')
        if not self.name:
            raise RpmException('No defined name in RequiresToken')
        string = self.prefix + self.name
        if self.version and not self.operator:
            raise RpmException('Have defined version and no operator %s' % self.version)
        if self.version:
            self.operator = self._format_operator(self.operator)
            string += ' ' + self.operator + ' ' + self.version

        return string
