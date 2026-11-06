Name:           dep-backslash-continuation-onelinecond-negated
Version:        1.0
Release:        0
Summary:        Test
License:        MIT
BuildRequires:  foo \
%{!?with_bar:BuildRequires: baz}

%description
Test.

%files

%changelog
