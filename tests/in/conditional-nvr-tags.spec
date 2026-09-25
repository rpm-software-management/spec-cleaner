%if "%{flavor}" == "test"
Name:           conditional-nvr-test
%else
Name:           conditional-nvr
%endif
%if 0%{?suse_version} >= 1600
Version:        2.0
%else
Version:        1.0
%endif
%if %{with preview}
Release:        0%{?dist}
%else
Release:        3%{?dist}
%endif
Summary:        Test conditional Name, Version and Release tags
License:        MIT
URL:            https://example.org/
Source0:        %{name}-%{version}.tar.gz
Requires:       libfoo = %{version}-%{release}
Provides:       %{name}-compat = %{version}

%description
Test.

%changelog
