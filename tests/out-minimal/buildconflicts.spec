Name:           buildconflicts
BuildRequires:  compiler
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(libacl)
BuildConflicts: pkgconfig(aa) >= 1.0
#!BuildConflicts: libacl-devel
#!BuildConflicts: pkg-config
# the build service must not use an old rpmlint for this package
#!BuildConflicts: rpmlint-mini < 2.9.0

%changelog
