from .rpmexception import RpmException

class RpmRequiresToken(object):
    """
    Class containing informations about the dependency token
    Can be used to specify all the values present on the line
    Later on we use this to do various conversions
    
    prefix            name          comparator version
    BuildRequires:    boringpackage >=         5.2.8
    """
    
    name = None
    comparator = None
    version = None
    prefix = None
    
    def __init__(self, name, comparator = None, version = None, prefix = None):
        self.prefix = prefix
        self.name = name
        self.comparator = comparator
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
        if self.version and not self.comparator:
            raise RpmException('Have defined version and no comparator %s' % self.version)
        if self.version:
            string += ' ' + self.comparator + ' ' + self.version
        
        return string
