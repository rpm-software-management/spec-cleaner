BuildRequires:  pkgconfig
BuildConflicts: pkgconfig(pkg-config)
Requires:       pkgconfig

%description
Test.

%package pkg-config
Summary:        pkg-config compatibility
Conflicts:      pkg-config
Provides:       pkg-config = 0.29.2+1
Obsoletes:      pkg-config < 0.29.2+1
Provides:       pkgconfig = 0.29.2+1
Provides:       pkgconfig(pkg-config) = %{version}

%description pkg-config
Compatibility package.

%changelog
