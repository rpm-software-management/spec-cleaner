%install
make install

%post -n libfoo1 -p /sbin/ldconfig

%postun -n libfoo1 -p /sbin/ldconfig

%post
/sbin/ldconfig || :

%files
%{_libdir}/libfoo.so.1

%changelog
