Name:           python-foo
Version:        1.0
Release:        0
Summary:        Foo
License:        MIT
BuildRequires:  python-rpm-macros
%if 0%{?suse_version} > 1500
%{?sle15_python_module_pythons}
BuildRequires:  %{python_module setuptools}
%endif
%python_subpackages

%description
Foo.

%changelog
