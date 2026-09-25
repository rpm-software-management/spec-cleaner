Name:           global-late-multiline-condition
Version:        1.0
Release:        0
%global tarver %{version}
%{?with_foo:
%global fooflags --foo-%{tarver}
BuildRequires:  bar
}
%define plain 1
Summary:        Test a multi-line conditional block moves whole
License:        MIT
URL:            https://example.org
Source:         foo-%{tarver}.tar.gz

%description
Test.

%changelog
