%define _prefix /opt/foo
Name:           foo
Version:        1.0
Release:        0
Summary:        Test package
License:        MIT
URL:            https://example.org/foo

%description
Test package.

%install
mkdir -p %{buildroot}/usr/bin
ln -s %{_prefix}/bin/foo %{buildroot}/usr/bin/foo
install -D -m 0644 foo.desktop %{buildroot}/usr/share/applications/foo.desktop
install -D -m 0644 foo.service %{buildroot}%{_prefix}/lib/systemd/system/foo.service

%files
%{_prefix}
/usr/bin/foo
/usr/share/applications/foo.desktop

%changelog
