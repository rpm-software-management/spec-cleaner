%install
make install

%ldconfig_scriptlets libfoo1
%ldconfig_scriptlets -n libbar1

%post -n libfoo1 -p /sbin/ldconfig
%postun -n libfoo1 -p /sbin/ldconfig

%post libbar1 -p /sbin/ldconfig
%postun libbar1 -p /sbin/ldconfig

%{ldconfig_scriptlets -n libbaz1}

%post -n libbaz1 -p /sbin/ldconfig
%postun -n libbaz1 -p /sbin/ldconfig

%changelog
