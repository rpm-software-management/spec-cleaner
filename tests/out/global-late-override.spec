Name:           global-late-override
Version:        2.0.1
Release:        0
%global srcver %{version}
%if 0%{?sle_version} == 150400
%global srcver 1.9
%endif
%global docver %{version}
%{?snapshot:%global docver %{snapshot}}
Summary:        Test a redefinition of a late global stays below it
License:        MIT
URL:            https://example.org
Source:         foo-%{srcver}.tar.gz
Provides:       docver(%{docver})

%description
Test.

%changelog
