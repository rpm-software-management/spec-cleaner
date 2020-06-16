Source1: something
Source2: somethingelse
NoSource: 2
Source200: ou
NoSource: 300
Source300: godknowswhat
Source400:         https://files.pythonhosted.org/packages/py2.py3/i/ipyleaflet/ipyleaflet-%{version}-py2.py3-none-any.whl

%prep
%setup -q
cp %{S:1} %{buildroot}
cp %{S:2} %{buildroot}
cp %{S:200} %{buildroot}
cp %{S:300} %{buildroot}
