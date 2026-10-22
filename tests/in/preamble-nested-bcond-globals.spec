%if 0%{?suse_version} != 1110
%if %{with python_singlespec}
%bcond_with python
%bcond_with python3
%else
%bcond_without python3
%bcond_without python
%endif
%bcond_without ruby
%bcond_without perl
%else
%bcond_with python3
%bcond_with python
%bcond_with ruby
%bcond_with perl
%endif

Name:           preamble-nested-bcond-globals
Version:        0.7.40
Release:        0
Summary:        Package dependency solver
License:        BSD-3-Clause
Group:          Development/Libraries/C and C++
URL:            https://example.org/preamble-nested-bcond-globals
Source:         preamble-nested-bcond-globals-%{version}.tar.bz2
BuildRequires:  cmake >= 3.5
BuildRequires:  gcc-c++
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%if %{with ruby}
%global ruby_vendorarch %(ruby -r rbconfig -e "puts RbConfig::CONFIG['vendorarchdir']")
BuildRequires:  ruby-devel
BuildRequires:  swig
%endif

%if %{with python}
%global python_sitearch %(python3 -c "from sysconfig import get_path; print(get_path('platlib'))")
BuildRequires:  python3-devel
%endif

%description
Package dependency solver.

%changelog
