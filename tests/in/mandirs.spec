%files
%defattr(-,root,root)
%{_mandir}/man3/%{name}.3.gz
%{_mandir}/man5/%{name}.5.*
%{_mandir}/man1/%{name}.1%{ext_man}
%{_infodir}/%{name}.info.gz
%{_infodir}/%{name}.info.*

%files extension
%{_mandir}/man1/binary.1.gz

%files glob1
%{_mandir}/man1/binary.*

%files glob2
%{_mandir}/man?/binary*
