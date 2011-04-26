# enum that holds .spec file section types

class Section:

    PKG = (object(),)
    DESC = (object(),)
    PREP = (object(),)
    BUILD = (object(),)
    INSTALL = (object(),)
    CLEAN = (object(),)
    FILES = (object(),)
    CHANGELOG = (object(),)

    POST = (object(),)
    POSTUN = (object(),)
    PRE = (object(),)
    PREUN = (object(),)

    SCRIPTLETS = POST + POSTUN + PRE + PREUN

    CODE = PREP + BUILD + INSTALL + CLEAN + SCRIPTLETS

    ALL = PKG + DESC + PREP + BUILD + INSTALL + CLEAN + FILES + CHANGELOG + SCRIPTLETS
