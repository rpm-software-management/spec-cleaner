Name:           brackety-package-names
Version:        1.0
Release:        0
Summary:        Test
License:        MIT
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(libxml-2.0)
Requires:       pkgconfig(zlib)
%requires_eq    zlib-devel
%requires_ge    libxml2-devel
Provides:       zlib-devel = %{version}
Obsoletes:      zlib-devel < %{version}

%description
Test.

%package devel
Summary:        Devel files
Requires:       pkgconfig(libxml-2.0)
Provides:       libxml2-devel = %{version}
Obsoletes:      libxml2-devel < %{version}

%description devel
Devel files.

%files

%files devel

%changelog
