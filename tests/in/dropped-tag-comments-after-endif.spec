Name:           dropped-tag-comments-after-endif
Version:        1.0
Release:        0
Summary:        Test
License:        MIT
URL:            https://example.com
Source:         foo.tar.gz
# kept note

BuildRequires:  gcc
# the packager is set by OBS
Packager:       Someone
%if 0%{?suse_version}
BuildRequires:  bar
# inner trailing note

%endif
# the vendor is set by OBS
Vendor:         Someone
BuildRequires:  baz
%if 0%{?is_opensuse}
Requires:       qux
# note before else

%else
# needed for SLE 11
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:       quux
%endif

%description
Test.

%files

%changelog
