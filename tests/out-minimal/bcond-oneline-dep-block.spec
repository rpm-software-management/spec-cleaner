# A conditional dependency reading a bcond keeps its define block below the bconds
Name:           bcond-oneline-dep-block
Version:        1.0
Release:        0
Summary:        Test
License:        MIT
%if 0%{?suse_version}
%define flavor suse
%{?with_foo:BuildRequires:  baz}
%endif
%bcond_with foo

%description
Test.

%files

%changelog
