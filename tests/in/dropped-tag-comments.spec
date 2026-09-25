Name:           dropped-tag-comments
Version:        1.0
Release:        0
Summary:        Test
License:        MIT
URL:            https://example.com
Source:         foo.tar.gz
# needed for SLE 11
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:       zzz
# build dependencies

# the vendor is set by OBS
Vendor:         Someone
BuildRequires:  gcc
Requires:       aaa

%description
Test.

%package devel
Summary:        Devel files
# same license as the main package
License:        MIT
Requires:       %{name} = %{version}

%description devel
Devel files.

%files

%files devel

%changelog
