%install
install bla

%ifarch x86
%files -n something
%defattr(-,root,root)
/bin/bla
%endif

%changelog
