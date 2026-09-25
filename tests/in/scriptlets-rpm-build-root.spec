%install
install -D -m 0755 foo $RPM_BUILD_ROOT%{_sbindir}/foo-setup

%post
test -x $RPM_BUILD_ROOT%{_sbindir}/foo-setup && $RPM_BUILD_ROOT%{_sbindir}/foo-setup
if [ -z "$RPM_BUILD_ROOT" ]; then echo ok; fi

%preun
rm -rf ${RPM_BUILD_ROOT}/var/cache/foo

%triggerin -- bar
ls $RPM_BUILD_ROOT/etc

%filetriggerin -- /usr/lib
ls $RPM_BUILD_ROOT/etc

%files
%{_sbindir}/foo-setup
