%files
%{_datadir}/foo
%defattr(-,nobody,nobody)
%{_localstatedir}/lib/foo
%defattr(-,root,root)
%{_bindir}/foo

%files doc
%defattr(0644,root,root,0755)
%doc README
%defattr(-,root,root,-)
%{_bindir}/foo-doc

%changelog
