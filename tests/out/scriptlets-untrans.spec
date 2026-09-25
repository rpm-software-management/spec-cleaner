%install
touch %{buildroot}/x

%preuntrans
if [ $1 -eq 0 ]; then rm -f %{_localstatedir}/lib/foo/cache; fi

%postuntrans
%{_bindir}/foo-cleanup --all

%preuntrans -n libfoo1 -p /sbin/ldconfig
%postuntrans -n libfoo1 -p /sbin/ldconfig

%files
/x

%changelog
