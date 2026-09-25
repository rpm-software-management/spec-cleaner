%define modname Foo
%define modname_lower foo
%global python2_wheelname %{modname}-%{version}-py2.py3-none-any.whl
Name:           python-%{modname}
Version:        1.0
Source0:        https://pypi.io/packages/source/F/Foo/%{modname}-%{version}.tar.gz
