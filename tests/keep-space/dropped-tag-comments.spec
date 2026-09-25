Name:           dropped-tag-comments
Version:        1.0
Release:        0
Summary:        Test
License:        MIT
URL:            https://example.com
Source:         foo.tar.gz
# build dependencies

BuildRequires:  gcc
Requires:       aaa
Requires:       zzz

%description
Test.

%package devel
Summary:        Devel files
Requires:       %{name} = %{version}

%description devel
Devel files.

%files

%files devel

%changelog
