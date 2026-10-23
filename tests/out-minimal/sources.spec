Source1:        something
Source2:        somethingelse
Source200:      ou
Source300:      godknowswhat
Source400:      https://files.pythonhosted.org/packages/py2.py3/i/ipyleaflet/ipyleaflet-%{version}-py2.py3-none-any.whl
NoSource:       2
NoSource:       300

%prep
%setup -q
cp %{S:1} %{buildroot}
cp %{S:2} %{buildroot}
cp %{S:200} %{buildroot}
cp %{S:300} %{buildroot}
cp %{P:1} %{buildroot}

%changelog
