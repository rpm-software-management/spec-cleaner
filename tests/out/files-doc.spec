%files
%{_mandir}/man1/remind.1%{?ext_man}
%{_mandir}/man1/rem2ps.1%{?ext_man}
%{_mandir}/man3/Remind::PDF.3pm%{ext_man}
%{_mandir}/man1/%{progname}.1%{?ext_man}
%{_mandir}/man3/*.3%{?ext_man}
%{_infodir}/%{name}.info%{?ext_info}
%doc AUTHORS ChangeLog FAQ NEWS README RELNOTES THANKS
%license LICENCE
%license COPYING
%doc AUTHORS ChangeLog README
%doc %{_mandir}/man1/mixed.1%{ext_man} README.mixed
%docdir %{_defaultdocdir}/%{name}
%{_mandir}/man1/plain.1%{?ext_man}
%{_bindir}/remind

%changelog
