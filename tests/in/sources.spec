Source1: something
Source2: somethingelse
NoSource: 2
Source200: ou
NoSource: 300
Source300: godknowswhat

%prep
%setup -q
cp %{S:1} %{buildroot}
cp %{S:2} %{buildroot}
cp %{S:200} %{buildroot}
cp %{S:300} %{buildroot}
