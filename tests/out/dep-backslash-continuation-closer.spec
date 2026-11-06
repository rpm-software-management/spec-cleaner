Name:           dep-backslash-continuation-closer
Version:        1.0
Release:        0
Summary:        Test
License:        MIT
BuildRequires:  after
%{?with_foo:
BuildRequires:  bar
}

%description
Test.

%files

%changelog
