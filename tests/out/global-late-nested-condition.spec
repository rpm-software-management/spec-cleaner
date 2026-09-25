%bcond_with docs
Name:           globalnested
Version:        1.0
Release:        0
%if 0%{?suse_version} > 1500
%global tarver %{version}
%else
%global tarver %(echo %{version} | tr '~' '-')
%endif
%if %{with docs}
%if 0%{?suse_version}
%global docver %{version}
%endif
%endif
Summary:        Nested global order
License:        MIT
URL:            https://example.org
Source:         foo-%{tarver}.tar.gz
BuildRequires:  bar >= %{tarver}
Requires:       baz = %{tarver}

%description
Test.

%changelog
