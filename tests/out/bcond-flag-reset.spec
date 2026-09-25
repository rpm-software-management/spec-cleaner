%if 0%{?suse_version} >= 1500
%define y_default 1
%else
%define y_default 0
%endif
%define soname 1
%bcond_without foo
%bcond y %{y_default}
%if 0%{?suse_version} >= 1500
%bcond_without tests
%endif
%if %{with foo}
%define doc_opts --enable-docs
%endif
Name:           bcond-flag-reset
Version:        1.0
Release:        0
Summary:        Test the bcond flag reset between conditions
License:        MIT
URL:            https://example.com
Source:         foo-%{version}.tar.gz
%if %{with y}
BuildRequires:  ybuild
%endif

%description
Test.

%prep
%autosetup

%build
%configure %{?doc_opts}

%install

%files

%changelog
