%install
/bin/rm %{buildroot}%{_libdir}/*.la
find "$b" -iname "*.la" -delete;
find "$b/%_libdir" -maxdepth 1 -type f -name "*.la" -delete;
find "$b/%_libdir" -type f -name "*.la" -delete
find "$b/%_libdir" -type f -name "*.la" -delete;
find "$b" -name "*.la" -delete
find "$b/%_prefix" -iname "*.la" -delete;
find "$b" -type f -iname "*.la" -delete;
find "$b" -type f -name "*.la" -delete
find "$b" -type f -name "*.la" -delete;
find "$b" -type f -name "*.la" -print -delete
    find %{buildroot}/$dir \( -name '*.py[co]' -o -name '*.la' \) -print0 | xargs -0 rm
find %{buildroot}/%{_libdir}/gedit/plugins -name "*.la" -delete -print
find %{buildroot}%{_libdir}/gedit/plugins/ -type f -name "*.la" -delete -print
find %{buildroot}%{_libdir} -name "*.la" -delete
find %{buildroot}%{_libdir} -name '*.la' -delete
find  %{buildroot}%{_libdir} -name '*.la' -delete -print
find %{buildroot}%{_libdir} -name "*.la" -delete -print
find %{buildroot}%{_libdir} -name '*.la' -delete -print
find %{buildroot}%{_libdir} -name '*.la' -delete -print >/dev/null 2>&1 ||
find %{buildroot}/%{_libdir} -name '*.la' -exec rm {} \;
find %{buildroot}%{_libdir} -name '*.la' -exec rm {} \;
find %{buildroot}%{_libdir} -name \*.la -exec rm '{}' \;
find %{buildroot}%{_libdir} -name '*.la' -exec rm -f {} +
find %{buildroot}%{_libdir} -name '*.la' -exec rm -v {} \;
find %{buildroot}%{_libdir} -name '*.la' -exec rm -v {} +
find %{buildroot}%{_libdir} -name '*.la' -exec rm -vf {} \;
find %{buildroot}%{_libdir} -name "*.la" -type f -delete -print
find %{buildroot}%{_libdir} -name '*.la' -type f -delete -print
find %{buildroot}%{_libdir} -name "*.la" -type f -print -delete
find %{buildroot}%{_libdir} -name '*.la' | xargs rm -f
find %{buildroot}%{_libdir}/%{pkg_name}/ -type f -name \*.la -print0 | xargs -r0 rm -fv
find %{buildroot}%{_libdir}/stardict/plugins -name "*.la" -print0 | xargs -0 rm -rf {} \;
find "%buildroot/%_libdir" -type f -name "*.la" -delete
  find %{buildroot}%{_libdir} -type f -name '*.la' -delete -print
find %{buildroot}%{_libdir} -type f -name "*.la" -delete -print
find %{buildroot}%{_libdir} -type f -name '*.la' -delete -print
find %{buildroot}%{_libdir} -type f -name "*.la" -print -delete
find %{buildroot}%{_libdir} -type f -name '*.la' -print -delete
find "%buildroot/%_libdir" -type f -name "*.la" | xargs rm -f
find %{buildroot}%{_libdir}/xorg/modules/ -name "*.la" | \
find "%buildroot" -name "*.la" -delete
find %buildroot -name '*.la' -delete
find %{buildroot} -name "*.la" -delete
find %{buildroot} -name '*.la' -delete
find %{buildroot} -name *.la -delete
find %buildroot -name "*.la" -delete -print
find %{buildroot} -name "*.la" -delete -print
find %{buildroot} -name '*.la' -delete -print
find %{buildroot} -name \*.la -delete -print
find %{buildroot} -name '*.la' -exec rm {} \;
find %{buildroot} -name *.la -exec rm '{}' +
find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name '*.la' -exec rm -f {} \;
find %{buildroot} -name \*.la -exec rm -f {} \;
find "%buildroot" -name "*.la" -type f -delete
find %{buildroot} -name '*.la' -type f -delete
find %{buildroot} -name '*.la' -type f -delete -print
find %{buildroot} -name "*.la" -type f -print -delete
find %{buildroot} -name '*.la' -type f -print0 | xargs -0 rm -f
find "%buildroot" -type f -name "*.la" -delete
find "%buildroot" -type f -name "*.la" -delete;
find "%{buildroot}" -type f -name "*.la" -delete
find %buildroot -type f -name '*.la' -delete
find %{buildroot} -type f -name '*.la' -delete
find %{buildroot} -type f -name *.la -delete
find %{buildroot} -type f -name "*.la" -delete -print
find %{buildroot} -type f -name '*.la' -delete -print
find "%{buildroot}" -type f -name '*.la' -exec %__rm {} \;
find %{buildroot} -type f -name *.la -exec rm {} \;
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'
find %{buildroot} -type f -name '*.la' -exec rm -f {} ';'
find %{buildroot} -type f -name "*.la" -exec %{__rm} -fv {} +
find %{buildroot} -type f -name "*.la" -exec %{__rm} -vf {} +
find "%buildroot" -type f -name "*.la" -print -delete
find %{buildroot} -type f -name "*.la" -print -delete
find %{buildroot} -type f -name "*.la" -print0 | xargs -0 rm -f
find %{buildroot} -type f -name "*.la" | xargs rm
find %{buildroot} -type f -name "*.la" | xargs rm -vf
find $RPM_BUILD_ROOT%{_libdir} -name *.la | xargs rm -f
find $RPM_BUILD_ROOT/%{_libdir} -name \*.la | xargs rm -fv
find $RPM_BUILD_ROOT \( -name "*.a" -o -name "*.la" \) -delete
find $RPM_BUILD_ROOT -name '*.la' -delete
find $RPM_BUILD_ROOT -name "*.la" -exec rm {} \;
find $RPM_BUILD_ROOT -name \*.la -exec rm {} \;
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name '*.la' -or -name '*.a' | xargs rm -f
find $RPM_BUILD_ROOT -name '*.la' -or -name '*.a' | xargs rm -v
find $RPM_BUILD_ROOT -name "*.la" -print -delete
find $RPM_BUILD_ROOT -name '*.la' -type f -print0 | xargs -0 rm -f
find $RPM_BUILD_ROOT -name '*.la' | xargs rm -f
find $RPM_BUILD_ROOT -type f -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.la" -exec %{__rm} -fv {} +
rm %buildroot/%_libdir/beaver/plugins/*.la
rm %{buildroot}%{_libdir}/claws-mail/plugins/*.la
rm %{buildroot}%{_libdir}/grisbi/*.la
rm %{buildroot}%{_libdir}/gstreamer-%{gst_branch}/*.la
rm "%buildroot/%_libdir"/*.la
rm "%{buildroot}%{_libdir}"/*.la
rm %buildroot/%{_libdir}/*.la
rm %buildroot/%_libdir/*.la
rm %buildroot%_libdir/*.la
rm %{buildroot}/%{_libdir}/*.la
rm %{buildroot}%{_libdir}/*.la
rm %{buildroot}%{_libdir}/*/*.la
rm %{buildroot}%_libdir/*.la
%{__rm} %{buildroot}/%{_libdir}/*.la
%{__rm} %{buildroot}%{_libdir}/*.la
%__rm "%{buildroot}%{_libdir}"/*.la
%__rm %buildroot/%_libdir/*.la
%__rm %buildroot/%_libdir/*/*.la
%__rm %buildroot/%_libdir/*/*/*.la
%__rm %{buildroot}%{_libdir}/*.la
rm  %{buildroot}/%{_libdir}/lib*.la
rm %{buildroot}%{_libdir}/lib*.la
%__rm %{buildroot}%{_libdir}/lib*.la
rm %{buildroot}/%{_libdir}/%{name}/%{version}/*.la
rm %{buildroot}%{_libdir}/purple-?/*.la
rm %{buildroot}%{_libdir}/sane/libsane-*.la
rm %{buildroot}/%{_libdir}/syslog-ng/*.la
rm %{buildroot}%{_libdir}/xfce4/panel/plugins/*.la
rm -f "$b/%_libdir"/*.la
%{__rm} -f %{buildroot}%{_libdir}/caca/*.la
rm -f %{buildroot}%{_libdir}/dssi/*.la
rm -f %{buildroot}%{_libdir}/glade3/modules/*.la
rm -f %{buildroot}%{_libdir}/gtk-*/*/*engines/*.la
rm -f %{buildroot}/%{_libdir}/gtk-3.0/3.0.0/immodules/*.la
rm -f %{buildroot}%{_libdir}/hexchat/plugins/*.la
rm -f "%buildroot/%_libdir"/*.la
rm -f "%buildroot/%_libdir"/*.la;
rm -f "%{buildroot}/%{_libdir}"/*.la
rm -f %buildroot%_libdir/*.la
rm -f %{buildroot}/%{_libdir}/*.la
rm -f %{buildroot}/%{_libdir}/*.la \
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/*.la \
rm -f %{buildroot}%{_libdir}/*/*/*.la
rm -f %{buildroot}%_libdir/*.la
%{__rm} -f %{buildroot}%{_libdir}/*.la
%__rm -f "%{buildroot}%{_libdir}"/*.la
%__rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/*.la %{buildroot}%{_libdir}/sox/*.la
rm -f "%buildroot/%_libdir"/*.la "%buildroot/%_libdir/weston"/*.la;
rm -f %{buildroot}%{_libdir}/*.la %{buildroot}%{_libdir}/xfce4/session/splash-engines/*.la
%__rm -f "%{buildroot}/%{_libdir}"/{lftp/*/,}*.la
rm -f %{buildroot}%{_libdir}/libcc*.la
rm -f %{buildroot}%{_libdir}/libccscript*.la
rm -f %{buildroot}%{_libdir}/libfcgi*.la
rm -f %{buildroot}%{_libdir}/libglade/2.0/*.la
rm -f %{buildroot}/%{_libdir}/lib*.la
rm -f %{buildroot}%{_libdir}/lib*.la
%{__rm} -f %{buildroot}%{_libdir}/libnfsidmap/*.la
rm -f %{buildroot}%{_libdir}/librdf*.la
rm -f %{buildroot}%{_libdir}/m17n/*/*.la
rm -f %{buildroot}%{_libdir}/%{name}{,/modules,/plugins}/*.la
rm -f %{buildroot}%{_libdir}/parole-0/*.la
rm -f %{buildroot}%{_libdir}/rpm-plugins/*.la
rm -f %{buildroot}%{_libdir}/scim-1.0/%{scim_binary_version}/*/*.la
rm -f %{buildroot}%{_libdir}/smsd/*.la
rm -f "%buildroot/%_lib/security"/*.{a,la} "%buildroot/%_libdir"/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/alsa-lib/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/cmpi/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT/%_libdir/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f ${RPM_BUILD_ROOT}/%{_libdir}/*.la
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/ladspa/*.la
rm -f  $RPM_BUILD_ROOT%{_libdir}/lib*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la
%__rm -f ${RPM_BUILD_ROOT}/%{_libdir}/lib*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/connection-driver/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{name}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/lock-driver/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/openwsman/authenticators/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/openwsman/plugins/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/scim-1.0/%{scim_binary_version}/*/*.la
rm -f $RPM_BUILD_ROOT/%_libdir/stonith/plugins/stonith2/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/tsclient/plugins/*.la
rm -f $RPM_BUILD_ROOT/%_lib/security/*.la
rm -fv %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}/%{_libdir}/*.la
rm -rf %{buildroot}%{_libdir}/*.la
%{__rm} -rf %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_libdir}/moc/decoder_plugins/*.la
rm -rf %{buildroot}%{_libdir}/tls/*.la
rm -rf $RPM_BUILD_ROOT/%{_lib}/security/*.la
rm -rfv %{buildroot}%{_libdir}/pdns/*.la
rm $RPM_BUILD_ROOT/%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%_libdir/*.la
rm ${RPM_BUILD_ROOT}/%{_libdir}/*.la
rm ${RPM_BUILD_ROOT}%{_libdir}/lib*.la
rm $RPM_BUILD_ROOT/%{_libdir}/libpng*.la
rm $RPM_BUILD_ROOT/%{_libdir}/lksctp-tools/*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/pidgin/*.la
rm $RPM_BUILD_ROOT/%{_prefix}/%{_lib}/lib*.la
rm $RPM_BUILD_ROOT/usr/%_lib/*.la
rm -rv %{buildroot}%{_libdir}/*.la
rm -v %{buildroot}/%{_libdir}/*.la
rm -v %{buildroot}%{_libdir}/*.la
rm -v %{buildroot}%{_libdir}/ntrack/modules/*.la
%{__rm} -v %{buildroot}%{_libdir}/{,openhpi/}*.la
%{__rm} -v %{buildroot}/%{_lib}/*.la
    rm -vf   %{buildroot}%{_libdir}/*.la
rm -vf %{buildroot}%{_libdir}/*.la
%{__rm} -vf %{buildroot}%{_libdir}/*.la
%{__rm} -vf %{buildroot}%{_libdir}/%{pkg_name}/*.la
rm -fv %{buildroot}%{_libdir}/libapparmor.la %{buildroot}%{_libdir}/libimmunix.la
