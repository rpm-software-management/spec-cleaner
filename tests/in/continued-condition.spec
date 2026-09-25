%define srcname continued
%bcond_without docs
%if 0%{?suse_version} > 1500 || \
    %{with docs}
%define docfmt html
%endif
Name:           continued-condition
Version:        1.0
Release:        0
%if 0%{?suse_version} > 1500 || \
    0%{?sle_version} >= 150400
%global srcver v%{version}
%endif
Summary:        Test a condition continued with a backslash stays whole
License:        MIT
URL:            https://example.org
Source:         %{srcname}-%{?srcver}.tar.gz
%if 0%{?suse_version} > 1500 || \
    0%{?sle_version} >= 150400
BuildRequires:  bar
%endif
%if 0%{?suse_version} > 1600
BuildRequires:  a
%elif 0%{?sle_version} >= 150400 && \
      0%{?is_opensuse}
BuildRequires:  b
%endif
Provides:       docfmt(%{?docfmt})

%description
Test.

%changelog
