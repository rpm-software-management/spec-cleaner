Name:           foo
Version:        1.0
Release:        0
Summary:        Test package
License:        MIT
URL:            https://example.org
Source:         foo.tar.gz
# Section 3 of the upstream docs lists these
BuildRequires:  aaa-devel
BuildRequires:  python3-setuptools
BuildRequires:  zzz-devel
Requires:       baz
%if %{with tests}
# section below is only needed for the testsuite
BuildRequires:  python3-pytest
%endif

%description
Test package.

%files

%changelog
