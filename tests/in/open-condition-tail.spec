%bcond_without docs
Name:           python-open-condition-tail
Version:        1.0
Release:        0
Summary:        Test a block open at a section header follows the tail macros
License:        MIT
URL:            https://example.org
BuildRequires:  python-rpm-macros
BuildArch:      noarch
%python_subpackages

%if %{with docs}
%package doc
Summary:        Documentation

%description doc
Documentation.
%endif

%description
Test.

%changelog
