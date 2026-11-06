%install
make install

%post foo -p /sbin/ldconfig
%postun -n foo -p /sbin/ldconfig

%post -n bar -p /sbin/ldconfig
%postun bar -p /sbin/ldconfig

%post baz -p /sbin/ldconfig
%postun baz -p /sbin/ldconfig
