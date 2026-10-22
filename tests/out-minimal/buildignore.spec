Name:           buildignore
BuildRequires:  compiler
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(libacl)
BuildConflicts: pkgconfig(aa) >= 1.0
#!BuildIgnore:  libacl-devel
#!BuildIgnore:  pkg-config
#!BuildIgnore:  xerces-j2
#!BuildIgnore:  xml-commons
#!BuildIgnore:  xml-commons-apis
#!BuildIgnore:  xml-commons-resolver
BuildRoot: bla

%changelog
