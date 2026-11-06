Name:           dep-backslash-continuation-multilinecond
Version:        1.0
Release:        0
Summary:        Test
License:        MIT
BuildRequires:  foo
%{?with_foo:
BuildRequires:  bar
}

%description
Test.

%files

%changelog
