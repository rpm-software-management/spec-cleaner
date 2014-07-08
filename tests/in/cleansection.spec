%install
install bla

%clean
rm bla

%ifarch x86
%files -n something
/bin/bla
%endif
