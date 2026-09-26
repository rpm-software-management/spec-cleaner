%define __make make -j4
%global __python3 %{_bindir}/python3.11
%bcond_with clang
%if %{with clang}
%define __cc clang
%define __cxx clang++
%endif
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
gcc -E foo.cc
%{__python3} setup.py build
%{__python3} setup.py test
rm -f build.log

%files

%changelog
