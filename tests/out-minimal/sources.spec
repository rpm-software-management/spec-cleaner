Source1:        something
Source2:        somethingelse
Source200:      ou
Source300:      godknowswhat
NoSource:       2
NoSource:       300

%prep
%setup -q
cp %{SOURCE1} %{buildroot}
cp %{SOURCE2} %{buildroot}
cp %{SOURCE200} %{buildroot}
cp %{SOURCE300} %{buildroot}

%changelog
