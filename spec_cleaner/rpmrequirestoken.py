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

    def __init__(self, name, operator = None, version = None, prefix = None):
        self.prefix = prefix
        self.name = name
        self.operator = operator
        self.version = version

    def dump_token(self):
        """
        Output it all on nice pretty line
        """

        if not self.prefix:
            raise RpmException('No defined prefix in RequiresToken')
        if not self.name:
            raise RpmException('No defined name in RequiresToken')
        string = self.prefix + self.name
        if self.version and not self.operator:
            raise RpmException('Have defined version and no operator %s' % self.version)
        if self.version:
            string += ' ' + self.operator + ' ' + self.version

        return string
