%global flavor @BUILD_FLAVOR@%{nil}
%if "%{flavor}" == "test"
%global pkg_suffix -test
%endif
%global tarver %{version}
Name:           globalconditional%{?pkg_suffix}
Version:        1.0
Release:        0
%if 0%{?suse_version} > 1500
%define with_foo 1
%global srcver v%{version}
%endif
Summary:        Conditional global order
License:        MIT
URL:            https://example.org
Source:         foo-%{tarver}.tar.gz

%description
Test.

%changelog
