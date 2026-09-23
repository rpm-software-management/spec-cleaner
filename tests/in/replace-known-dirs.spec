%install
install -D -m 0644 %{name}.service %{buildroot}/usr/lib/systemd/system/%{name}.service
install -D -m 0644 %{name}.tmpfiles %{buildroot}/usr/lib/tmpfiles.d/%{name}.conf
install -D -m 0644 %{name}.sysusers %{buildroot}/usr/lib/sysusers.d/%{name}.conf
install -D -m 0644 99-%{name}.rules %{buildroot}/usr/lib/udev/rules.d/99-%{name}.rules
install -D -m 0644 %{name}.sysctl %{buildroot}/usr/lib/sysctl.d/99-%{name}.conf
install -D -m 0644 Module.pm %{buildroot}/usr/lib/perl5/vendor_perl/Module.pm
install -D -m 0644 %{name}.el %{buildroot}/usr/share/emacs/site-lisp/%{name}.el
install -D -m 0644 %{name}.ttf %{buildroot}/usr/share/fonts/%{name}.ttf
install -D -m 0644 %{name}.cmxs %{buildroot}/usr/lib64/ocaml/%{name}.cmxs
install -D -m 0644 %{name} %{buildroot}/etc/apparmor.d/%{name}
cp -a package.json %{buildroot}/usr/lib/node_modules/%{name}/

%files
%{_unitdir}/%{name}.service
/usr/lib/systemd/system/legacy.service
%{_prefix}/lib/systemd/system/already.service
%{_tmpfilesdir}/%{name}.conf
%{_sysusersdir}/%{name}.conf
%{_udevrulesdir}/99-%{name}.rules
%{_sysctldir}/99-%{name}.conf
%dir /usr/lib/tmpfiles.d
%{perl_vendorlib}/Module.pm
/usr/lib/perl5/vendor_perl/Other.pm
%{_emacs_sitelispdir}/%{name}.el
/usr/share/emacs/site-lisp/legacy.el
%{_datadir}/emacs/site-lisp/premacroed.el
%{_fontsdir}/%{name}.ttf
%dir /usr/share/fonts
%{ocaml_standard_library}/%{name}.cmxs
/usr/lib64/bar.so
%{apparmor_profilesdir}/%{name}
/etc/apparmor.d/legacy
%{nodejs_sitelib}/%{name}/
