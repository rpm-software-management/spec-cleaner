%bcond_with clang
%if %{with clang}
%define __cc clang
%define __cxx clang++
%endif
%global __python3 /usr/bin/python3.11
Name:           foo
Version:        1.0
Release:        0
Summary:        Test package
License:        MIT
URL:            https://example.org/foo

%description
Test package.

%build
export CC=%{__cc} CXX=%{__cxx}
%{__python3} setup.py build
%__python3 setup.py test
%{__rm} -f build.log

%files

%changelog
