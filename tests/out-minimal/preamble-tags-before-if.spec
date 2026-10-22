%define singlespec_py3 ( 0%{?suse_version} > 1330 )
Name:           preamble-tags-before-if
Version:        0.6.6
Release:        0
Summary:        Helper that makes writing plugins easier
License:        GPL-2.0-only
Group:          System/Packages
URL:            https://example.org/preamble-tags-before-if
Source0:        %{name}-%{version}.tar.bz2
BuildArch:      noarch
%if %{singlespec_py3}
BuildRequires:  %{python_module devel}
BuildRequires:  python-rpm-macros
# provide old names for py2 package
%if "%{python_flavor}" == "python2"
Obsoletes:      preamble-tags-before-if-python < %{version}-%{release}
Provides:       preamble-tags-before-if-python = %{version}-%{release}
%endif
%python_subpackages
%else
%define have_python2 1
%if ( 0%{?suse_version} == 1315 )
%define have_python3 1
%else
%define have_python3 0
%endif
%endif

%description
Helper that makes writing plugins easier.

%changelog
