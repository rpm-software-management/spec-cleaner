Name:           python-foo
Version:        1.0
Release:        0
Summary:        Foo
License:        MIT
BuildRequires:  python-rpm-macros
%if 0%{?suse_version} > 1500
%python_subpackages
%endif
%if %{with singlespec}
%python_subpackages
%else
Requires:       python3
%endif
%if %{with legacy}
%python_subpackages
# keep the legacy flavor
%endif

%description
Foo.

%changelog
