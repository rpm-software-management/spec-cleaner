Name:           dep-backslash-continuation-requires-eq
Version:        1.0
Release:        0
Summary:        Test
License:        MIT
BuildRequires:  foo
%requires_eq    libfoo
%requires_eq    libbar

%description
Test.

%files

%changelog
