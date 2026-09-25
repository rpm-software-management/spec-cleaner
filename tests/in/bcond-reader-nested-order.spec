%bcond_without foo
%if 0%{?suse_version}
%global foo_flag %{with foo}
%define foo_name foo
%global foo_level 2
%endif
Name:           bcond-reader-nested-order
Version:        1.0
Release:        0
Summary:        Test a nested level without bconds keeps its define order
License:        MIT
URL:            https://example.org/

%description
Test.

%build
echo %{?foo_flag} %{?foo_name} %{?foo_level}

%changelog
