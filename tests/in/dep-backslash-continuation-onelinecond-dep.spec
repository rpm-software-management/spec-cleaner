Name:           dep-backslash-continuation-onelinecond-dep
Version:        1.0
Release:        0
Summary:        Test
License:        MIT
BuildRequires:  foo \
%{?with_bar:Requires: baz}

%description
Test.

%files

%changelog
