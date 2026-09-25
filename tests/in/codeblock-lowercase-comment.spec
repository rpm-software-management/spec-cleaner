Name:           foo
Version:        1.0
Release:        0
Summary:        Test package
License:        MIT
URL:            https://example.org
Source:         foo.tar.gz
BuildRequires:  zzz-devel
%if %{with tests}
# section below is only needed for the testsuite
BuildRequires:  python3-pytest
%endif
BuildRequires:  python3-setuptools
Requires:       baz
# Section 3 of the upstream docs lists these
BuildRequires:  aaa-devel

%description
Test package.

%files
