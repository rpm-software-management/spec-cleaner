# A condition reading the version stays below the Version tag
Name:           global-late-version-condition
Version:        1.0
Release:        0
%if "%{version}" == "1.0"
%define x 1
%endif
Summary:        Test
License:        MIT

%description
Test.

%files

%changelog
