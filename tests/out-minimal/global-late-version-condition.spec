# A condition reading the version stays below the Version tag
Name:           global-late-version-condition
Version:        1.0
Release:        0
Summary:        Test
License:        MIT
%if "%{version}" == "1.0"
%define x 1
%endif

%description
Test.

%files

%changelog
