Name:           buildconflicts
BuildRequires:  pkgconfig(libacl)
# the build service must not use an old rpmlint for this package
#!BuildConflicts: rpmlint-mini < 2.9.0
BuildRequires:  compiler
BuildRequires:  pkgconfig
#!BuildConflicts: libacl-devel
#!BuildConflicts: pkg-config
BuildConflicts: pkgconfig(aa) >= 1.0

%changelog
