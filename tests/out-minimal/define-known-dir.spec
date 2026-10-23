%define _sysconfdir /etc
%define _localstatedir /var
%global _libexecdir %{_prefix}/libexec
%define _mandir %{_datadir}/man
Name:           foo
Version:        1.0
Release:        0
Summary:        Test package
License:        MIT
URL:            https://example.org/foo

%description
Test package.

%install
install -D -m 0644 foo.conf %{buildroot}/etc/foo.conf
install -D -m 0755 foo-helper %{buildroot}/usr/libexec/foo-helper
install -D -m 0644 foo.1 %{buildroot}/usr/share/man/man1/foo.1
mkdir -p %{buildroot}/var/lib/foo

%files
/etc/foo.conf
/usr/libexec/foo-helper
/usr/share/man/man1/foo.1%{?ext_man}
/var/lib/foo

%changelog
