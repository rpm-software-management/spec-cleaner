%global srcname requests
%global upstream_version 2.3.4
Name:           python-%{srcname}
Version:        %{upstream_version}
Release:        0
%global majmin %(echo %{version} | cut -d. -f1-2)
%global docdir %{srcname}-%{majmin}
%global unrelated foo
%if "%{majmin}" == "2.3"
%define newapi 1
%endif
Summary:        Global dependencies
License:        MIT
URL:            https://example.org
Source:         %{srcname}-%{version}.tar.gz
Requires:       %{docdir}

%description
Test.

%changelog
