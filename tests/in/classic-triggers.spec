%files
%{_bindir}/foo

%triggerin -- bash
if [ -x %{_bindir}/foo ]; then
    echo "a  b"
fi

%files sub
%{_bindir}/bar

%triggerpostun -n sub -- bar < 2
rm -f %{_sysconfdir}/x  %{_sysconfdir}/y

%triggerprein -- baz
    echo "x  y"

%triggerun -- qux
    echo "p  q"

%changelog
