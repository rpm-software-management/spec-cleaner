Name:           dep-backslash-continuation-onelinecond
Version:        1.0
Release:        0
Summary:        Test
License:        MIT
BuildRequires:  foo \
%{?with_bar:%define qux 1}

%description
Test.

%files

%changelog
