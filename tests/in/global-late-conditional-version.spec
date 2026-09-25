Name:           global-late-conditional-version
%if 0%{?suse_version} > 1500
Version:        2.0.1
%global shortver %(echo %{version} | cut -d. -f1-2)
%else
Version:        1.0.1
%global shortver %(echo %{version} | cut -d. -f1-2)
%endif
Release:        0
Summary:        Test a global stays below the Version tag of its own branch
License:        MIT
URL:            https://example.org
Source:         foo-%{version}.tar.gz
Provides:       short(%{shortver})

%description
Test.

%changelog
