Name:           dropped-tag-comments-after-endif
Version:        1.0
Release:        0
Summary:        Test
License:        MIT
URL:            https://example.com
Source:         foo.tar.gz
BuildRequires:  baz
# kept note

BuildRequires:  gcc
%if 0%{?suse_version}
BuildRequires:  bar
# inner trailing note

%endif
%if 0%{?is_opensuse}
Requires:       qux
# note before else

%else
Requires:       quux
%endif

%description
Test.

%files

%changelog
