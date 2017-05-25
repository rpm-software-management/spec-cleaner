Name:           python-subpackages
BuildRequires:  %{python_module foo}
%ifpython2
Requires:       python2-backports.abc
%endif
%python_subpackages

%description
bla bla

%changelog
