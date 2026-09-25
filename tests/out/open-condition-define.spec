%bcond_without docs
Name:           open-condition-define
Version:        1.0
Release:        0
Summary:        Test a block open at a section header keeps wrapping it
License:        MIT
URL:            https://example.org
BuildRequires:  gcc
%if %{with docs}
%global docdir %{_docdir}/%{name}-doc
%define docfmt html
BuildRequires:  sphinx

%package doc
Summary:        Documentation

%description doc
Documentation in %{docfmt}.
%endif

%description
Test.

%package -n libopen1
Summary:        Library
%if 0%{?suse_version}
%if %{with docs}
%global libdoc 1
Requires:       %{name}-doc

%package -n libopen-devel
Summary:        Devel

%description -n libopen-devel
Devel.
%endif
%endif

%description -n libopen1
Library.

%changelog
