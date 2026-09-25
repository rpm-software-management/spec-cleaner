Name:           global-late-bcond-block
Version:        1.2.3
Release:        0
%if 0%{?suse_version}
%global docname %{name}-doc
%bcond_without docs
%endif
%if %{with docs}
%define builddoc 1
%endif
%if 0%{?suse_version} > 1500
%global testver %(echo %{version} | cut -d. -f1-2)
%bcond_without tests
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
