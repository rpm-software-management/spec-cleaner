%install
export PATH="$PATH:%{_prefix}/sbin"
mkdir -p %{buildroot}/usr/sbin

%files
%defattr(-,root,root)
%doc ChangeLog README COPYING
/usr/name/
/usr/libexec/name/
/usr/lib64/name
/usr/share/data/name
/usr/include/name
/var/name
/usr/sbin/name
/usr/bin/name
/usr/share/man/name
/usr/share/info/name
/usr/share/doc/packages/name
/etc/init.d/name
%_exec_prefix/bla
