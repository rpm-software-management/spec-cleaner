%define srcname bcond-condition-define-order
%bcond_without foo
%if %{with foo}
%global backend foo
%else
%global backend bar
%endif
%global backend_upper %(echo %{backend} | tr a-z A-Z)
Name:           bcond-condition-define-order
Version:        1.0
Release:        0
Summary:        Test globals reading a bcond conditional block stay below it
License:        MIT
URL:            https://example.org/

%description
Test.

%files
%{_datadir}/%{backend_upper}

%changelog
