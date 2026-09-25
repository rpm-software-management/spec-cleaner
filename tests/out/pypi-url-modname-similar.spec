%define modname Foo
%define modname_lower foo
Name:           python-%{modname}
Version:        1.0
%global python2_wheelname %{modname}-%{version}-py2.py3-none-any.whl
Source0:        https://files.pythonhosted.org/packages/source/F/Foo/%{modname}-%{version}.tar.gz

%changelog
