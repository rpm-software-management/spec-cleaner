%install
export PATH="$PATH:%{_sbindir}"
mkdir -p %{buildroot}%{_sbindir}

%files
%license COPYING
%doc ChangeLog README
%{_prefix}/name/
%{_libexecdir}/name/
%{_libdir}/name
%{_datadir}/data/name
%{_includedir}/name
%{_localstatedir}/name
%{_sbindir}/name
%{_bindir}/name
%{_mandir}/name
%{_infodir}/name
%{_docdir}/name
%{_initddir}/name
%{_prefix}/bla

%changelog
