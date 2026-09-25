%define srcname bcond-reading
%global plain_value 1
%define lazy_flag %{?with_docs:1}
%bcond_without docs
%global docflag %{?with_docs:--enable-docs}
%{?with_docs:%global docs_subpkg 1}
%global docopts %{?docs_subpkg:--subpkg} %{docflag}
%if %{with docs}
%global docs_extra %{?docs_subpkg:extra}
%endif
Name:           bcond-reading
Version:        1.0
Release:        0
Summary:        Test globals reading a bcond stay below it
License:        MIT
URL:            https://example.org/

%description
Test.

%build
%configure %{docopts} %{?docs_extra}

%changelog
