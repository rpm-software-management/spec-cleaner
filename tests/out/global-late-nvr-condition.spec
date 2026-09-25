Name:           global-late-nvr-condition
Version:        2.0
Release:        0
%global major %(echo %{version} | cut -d. -f1)
%if %{major} >= 2
Epoch:          1
%endif
Summary:        Test a conditional tag reading a late global stays below it
License:        MIT
URL:            https://example.org/

%description
Test.

%changelog
