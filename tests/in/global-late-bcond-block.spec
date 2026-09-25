%if 0%{?suse_version}
%bcond_without docs
%global docname %{name}-doc
%endif
%if %{with docs}
%define builddoc 1
%endif
Name:           global-late-bcond-block
Version:        1.2.3
Release:        0
%if 0%{?suse_version} > 1500
%bcond_without tests
%global testver %(echo %{version} | cut -d. -f1-2)
%else
%bcond_with tests
%endif
%if %{with tests}
%global testflag --tests
%endif
Summary:        Test %{?builddoc:with docs}
License:        MIT
URL:            https://example.org
Source:         foo-%{version}.tar.gz
Provides:       testflag(%{?testflag}x)

%description
Test.

%changelog
