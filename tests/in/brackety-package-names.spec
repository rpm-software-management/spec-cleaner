Name:           brackety-package-names
Version:        1.0
Release:        0
Summary:        Test
License:        MIT
BuildRequires:  libxml2-devel
Requires:       zlib-devel
%requires_eq    zlib-devel
%requires_ge    libxml2-devel
Provides:       zlib-devel = %{version}
Obsoletes:      zlib-devel < %{version}

%description
Test.

%package devel
Summary:        Devel files
Requires:       libxml2-devel
Provides:       libxml2-devel = %{version}
Obsoletes:      libxml2-devel < %{version}

%description devel
Devel files.

%files

%files devel

%changelog
