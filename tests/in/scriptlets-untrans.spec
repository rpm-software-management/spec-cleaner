%install
touch %{buildroot}/x

%preuntrans
if [ $1 -eq 0 ]; then rm -f /var/lib/foo/cache; fi

%postuntrans
/usr/bin/foo-cleanup --all

%preuntrans -n libfoo1
/sbin/ldconfig

%postuntrans -n libfoo1 -p /sbin/ldconfig

%files
/x
