#
# spec-cleaner is a program for cleaning up spec files.
# It makes sure that the spec file follows the guidelines of openSUSE.
#
# Only the macros that more than one known directory rewrite depends on are
# redefined here, so those rewrites stay off while the rest keep running.
#
%define _prefix /usr
%define _exec_prefix %{_prefix}
%define _datadir %{_prefix}/share
%define _sysconfdir /etc
Name:           redefined-known-dirs
Version:        1.0
Release:        0
Summary:        Paths must survive when their macros are redefined
License:        MIT
URL:            https://example.org/redefined-known-dirs

%install
install -D -m 0644 %{name}.service %{buildroot}/usr/lib/systemd/system/%{name}.service
install -D -m 0644 %{name}.tmpfiles %{buildroot}/usr/lib/tmpfiles.d/%{name}.conf
install -D -m 0644 %{name}.sysusers %{buildroot}/usr/lib/sysusers.d/%{name}.conf
install -D -m 0644 99-%{name}.rules %{buildroot}/usr/lib/udev/rules.d/99-%{name}.rules
install -D -m 0644 %{name}.sysctl %{buildroot}/usr/lib/sysctl.d/99-%{name}.conf
install -D -m 0644 Module.pm %{buildroot}/usr/lib/perl5/vendor_perl/%{perl_version}/Module.pm
install -D -m 0644 %{name}.el %{buildroot}/usr/share/emacs/site-lisp/%{name}.el
install -D -m 0644 %{name}.ttf %{buildroot}/usr/share/fonts/%{name}.ttf
install -D -m 0644 %{name}.cmxs %{buildroot}/usr/lib64/ocaml/%{name}.cmxs
install -D -m 0644 %{name} %{buildroot}/etc/apparmor.d/%{name}
cp -a package.json %{buildroot}/usr/lib/node_modules/%{name}/
install -D -m 0644 %{name}.conf %{buildroot}%{_datadir}/%{name}/etc/%{name}.conf
install -D -m 0755 legacy.sh /usr/legacy.sh
install -D -m 0644 legacy.service /etc/init.d/legacy
install -D -m 0644 legacy.conf /etc/legacy.conf
install -D -m 0644 legacy.state %{_localstatedir}/log/legacy
install -D -m 0644 legacy.bin %{_prefix}/bin/legacy
install -D -m 0644 legacy.sbin %{_prefix}/sbin/legacy
install -D -m 0644 legacy.exec %{_prefix}/libexec/legacy
install -D -m 0644 legacy.h %{_prefix}/include/legacy.h
install -D -m 0644 legacy.1 %{_datadir}/man/man1/legacy.1
install -D -m 0644 legacy.info %{_datadir}/info/legacy.info
install -D -m 0644 legacy.txt %{_datadir}/doc/packages/legacy.txt
install -D -m 0644 legacy.rd %{_initddir}/legacy.rd
echo %{_exec_prefix}

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
/usr/lib/perl5/vendor_perl/%{perl_version}/Other.pm
/usr/lib/perl5/vendor_perl/Unversioned.pm
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
%{_datadir}/%{name}/etc/%{name}.conf
%dir %{_libdir}/%{name}/var

%changelog
