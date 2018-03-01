%files
%{_mandir}/man3/%{name}.3%{?ext_man}
%{_mandir}/man5/%{name}.5%{?ext_man}
%{_mandir}/man1/%{name}.1%{?ext_man}
%{_infodir}/%{name}.info%{?ext_info}
%{_infodir}/%{name}.info%{?ext_info}

%files extension
%{_mandir}/man1/binary.1%{?ext_man}

%files glob1
%{_mandir}/man1/binary.*

%files glob2
%{_mandir}/man?/binary*

%changelog
