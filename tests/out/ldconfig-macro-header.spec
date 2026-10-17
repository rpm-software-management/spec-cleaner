%install
%make_install

%ldconfig_scriptlets -n libfoo1

%post
/sbin/ldconfig || :

%files
%{_libdir}/libfoo.so.1

%changelog
