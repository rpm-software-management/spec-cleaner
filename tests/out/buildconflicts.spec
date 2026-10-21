Name:           buildconflicts
BuildRequires:  compiler
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(libacl)
BuildConflicts: pkg-config
# the build service must not use an old rpmlint for this package
BuildConflicts: rpmlint-mini < 2.9.0
BuildConflicts: pkgconfig(aa) >= 1.0
BuildConflicts: pkgconfig(libacl)

%changelog
