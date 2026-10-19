Name: buildconflicts
BuildRequires: libacl-devel
# the build service must not use an old rpmlint for this package
#!BuildConflicts:  rpmlint-mini < 2.9.0
BuildRequires: compiler
#!BuildConflicts:  libacl-devel pkg-config
BuildConflicts: pkgconfig(aa) >= 1.0
