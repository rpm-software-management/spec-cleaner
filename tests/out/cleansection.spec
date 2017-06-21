%install
install bla

%ifarch x86
%files -n something
/bin/bla
%endif

%changelog
