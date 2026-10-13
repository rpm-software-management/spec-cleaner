Name:           macro-license
Version:        1.0
Release:        0
Summary:        Test macro-generated subpackage licenses
License:        MIT

%package devel
Summary:        Development files

%description
Test package.

%description devel
Development files.

%define data_subpkg(c:n:) \
%define countrycode %{-c:%{-c*}} \
\
%package data-%{countrycode}\
Summary:      Data files\
BuildArch:    noarch\
License:      BSD-2-Clause AND CC0-1.0\
\
%description data-%{countrycode}\
Data files.\
\
%files data-%{countrycode}
%data_subpkg -c ar -n Argentina
%data_subpkg -c at -n Austria

%files

%files devel

%changelog
