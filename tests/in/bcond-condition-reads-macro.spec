%bcond_with system_x
%if %{with system_x}
%define x_ver 2
%endif
%if 0%{?x_ver} >= 2
%bcond_without feature_x
%endif
%define foo 1
%bcond_with system_y
%if %{with system_y}
%define y_ver 2
%endif
%if 0%{?y_ver} >= 2
%bcond_without feature_y
%endif
Name:           bcond-condition-reads-macro
Version:        1.2
Release:        0
%global major %(echo %{version} | cut -d. -f1)
%if %{major} > 1
%bcond_without new
%else
%bcond_with new
%endif
Summary:        Test bcond blocks reading macros defined below the bconds
License:        MIT
%if %{with feature_x}
BuildRequires:  feature-x
%endif
%if %{with feature_y}
BuildRequires:  feature-y
%endif
%if %{with new}
BuildRequires:  new
%endif

%description
Test.

%changelog
