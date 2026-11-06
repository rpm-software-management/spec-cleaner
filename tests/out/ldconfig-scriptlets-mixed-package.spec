%install
%make_install

%post foo -p /sbin/ldconfig
%postun -n foo -p /sbin/ldconfig
%post -n bar -p /sbin/ldconfig
%postun bar -p /sbin/ldconfig
%ldconfig_scriptlets baz

%changelog
