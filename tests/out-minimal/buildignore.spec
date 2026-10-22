Name:           buildignore
#!BuildIgnore:  xerces-j2
#!BuildIgnore:  xml-commons
#!BuildIgnore:  xml-commons-apis
#!BuildIgnore:  xml-commons-resolver
#!BuildIgnore:  libacl-devel
#!BuildIgnore:  pkg-config
BuildRoot: bla
BuildConflicts: pkgconfig(aa) >= 1.0
BuildRequires:  compiler
BuildRequires:  pkgconfig(libacl)
BuildRequires:  pkgconfig

%changelog
