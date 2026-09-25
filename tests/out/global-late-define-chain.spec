%define shortver %(echo %{version} | cut -d. -f1-2)
Name:           global-late-define-chain
Version:        1.2.3
Release:        0
%global tarname foo-%{version}
%global docdir %{_docdir}/foo-%{shortver}
Summary:        Test a global using a define that reads the version stays below it
License:        MIT
URL:            https://example.org
Source:         %{tarname}.tar.gz
Provides:       docdir(%docdir)

%description
Test.

%changelog
