#
# spec-cleaner is a program for cleaning up spec files.
# It makes sure that the spec file follows the guidelines of openSUSE.
#
# Every path macro the known directory rewrites depend on is redefined here, so
# none of the hardcoded paths in the body may be touched.
#
%define _prefix /usr
%define _exec_prefix %{_prefix}
%define _bindir %{_exec_prefix}/bin
%define _sbindir %{_exec_prefix}/sbin
%define _libexecdir %{_exec_prefix}/libexec
%define _includedir %{_prefix}/include
%define _datarootdir %{_prefix}/share
%define _datadir %{_datarootdir}
%define _mandir %{_datadir}/man
%define _infodir %{_datadir}/info
%define _docdir %{_datadir}/doc/packages
%define _sysconfdir /etc
%define _initddir %{_sysconfdir}/init.d
%define _localstatedir /var
%define _lib /lib
%define _libdir %{_prefix}%{_lib}
%define _unitdir %{_prefix}/lib/systemd
%define _tmpfilesdir %{_prefix}/lib/tmpfiles.d
%define _sysusersdir %{_prefix}/lib/sysusers.d
%define _udevrulesdir %{_prefix}/lib/udev/rules.d
%define _sysctldir %{_prefix}/lib/sysctl.d
%define _fontsdir %{_datadir}/fonts
%define _emacs_sitelispdir %{_datadir}/emacs/site-lisp
%define _initrddir %{_prefix}/lib/rd
%define perl_version 5.36.0
%define perl_vendorlib %{_prefix}/lib/perl5/vendor_perl/%{perl_version}
%define ocaml_standard_library %{_libdir}/ocaml
%define nodejs_sitelib %{_prefix}/lib/node_modules
%define apparmor_profilesdir %{_sysconfdir}/apparmor.d
Name:           redefined-known-dirs
Version:        1.0
Release:        0
Summary:        Paths must survive when their macros are redefined
License:        MIT
URL:            https://example.org/redefined-known-dirs

%description
Paths must survive when their macros are redefined.

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
install -D -m 0644 legacy.state /var/log/legacy
install -D -m 0644 legacy.bin %{_prefix}/bin/legacy
install -D -m 0644 legacy.sbin %{_prefix}/sbin/legacy
install -D -m 0644 legacy.exec %{_prefix}/libexec/legacy
install -D -m 0644 legacy.h %{_prefix}/include/legacy.h
install -D -m 0644 legacy.1 %{_datadir}/man/man1/legacy.1
install -D -m 0644 legacy.info %{_datadir}/info/legacy.info
install -D -m 0644 legacy.txt %{_datadir}/doc/packages/legacy.txt
install -D -m 0644 legacy.rd %{_initrddir}/legacy.rd
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
