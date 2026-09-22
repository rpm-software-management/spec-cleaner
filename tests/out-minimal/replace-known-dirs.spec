%install
install -D -m 0644 %{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -D -m 0644 %{name}.tmpfiles %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -D -m 0644 %{name}.sysusers %{buildroot}%{_sysusersdir}/%{name}.conf
install -D -m 0644 99-%{name}.rules %{buildroot}%{_udevrulesdir}/99-%{name}.rules
install -D -m 0644 %{name}.sysctl %{buildroot}%{_sysctldir}/99-%{name}.conf
install -D -m 0644 Module.pm %{buildroot}%{perl_vendorlib}/Module.pm
install -D -m 0644 %{name}.el %{buildroot}%{_emacs_sitelispdir}/%{name}.el
install -D -m 0644 %{name}.ttf %{buildroot}%{_fontsdir}/%{name}.ttf
install -D -m 0644 %{name}.cmxs %{buildroot}%{ocaml_standard_library}/%{name}.cmxs
install -D -m 0644 %{name} %{buildroot}%{apparmor_profilesdir}/%{name}
cp -a package.json %{buildroot}%{nodejs_sitelib}/%{name}/

%files
%{_unitdir}/%{name}.service
%{_unitdir}/legacy.service
%{_unitdir}/already.service
%{_tmpfilesdir}/%{name}.conf
%{_sysusersdir}/%{name}.conf
%{_udevrulesdir}/99-%{name}.rules
%{_sysctldir}/99-%{name}.conf
%dir %{_tmpfilesdir}
%{perl_vendorlib}/Module.pm
%{perl_vendorlib}/Other.pm
%{_emacs_sitelispdir}/%{name}.el
%{_emacs_sitelispdir}/legacy.el
%{_emacs_sitelispdir}/premacroed.el
%{_fontsdir}/%{name}.ttf
%dir %{_fontsdir}
%{ocaml_standard_library}/%{name}.cmxs
%{_libdir}/bar.so
%{apparmor_profilesdir}/%{name}
%{apparmor_profilesdir}/legacy
%{nodejs_sitelib}/%{name}/

%changelog
