Name:           buildignore
#!BuildIgnore:  xerces-j2 xml-commons xml-commons-apis xml-commons-resolver
#!BuildIgnore:  libacl-devel pkg-config
BuildRoot: bla
BuildConflicts: pkgconfig(aa) >= 1.0
BuildRequires:  compiler
BuildRequires:  pkgconfig(libacl)
BuildRequires:  pkgconfig

%changelog
