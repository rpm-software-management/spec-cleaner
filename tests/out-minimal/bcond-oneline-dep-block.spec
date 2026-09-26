# A conditional dependency reading a bcond keeps its define block below the bconds
%bcond_with foo
%if 0%{?suse_version}
%define flavor suse
%{?with_foo:BuildRequires:  baz}
%endif
Name:           bcond-oneline-dep-block
Version:        1.0
Release:        0
Summary:        Test
License:        MIT

%description
Test.

%files

%changelog
