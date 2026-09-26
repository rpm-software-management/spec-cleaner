# A one-line condition reading a version-dependent global stays below it
Name:           global-late-oneline-condition
Version:        1.0
Release:        0
Summary:        Test
License:        MIT
%global late %{version}
%{?late:%define x 1}
%{!?late:%define y 1}

%description
Test.

%files

%changelog
