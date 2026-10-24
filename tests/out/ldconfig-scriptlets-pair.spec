%install
%make_install

%ldconfig_scriptlets -n libs1
%ldconfig_scriptlets -n libt1

%preun
/sbin/baz

%postun -n libu1 -p /sbin/ldconfig
%preun -n libt1
/sbin/qux

%check
%make_build check

%ldconfig_scriptlets -n %{name}%{sover}

%post -n libtorch%{?pkg_suffix} -p /sbin/ldconfig
%postun -n libtorch%{?pkg_suffix} -p /sbin/ldconfig
%ldconfig_scriptlets
%ldconfig_scriptlets libs
%ldconfig_scriptlets -n libb1

%if %{with foo}
%ldconfig_scriptlets -n libc1
%endif

%post -n libd1 -p /sbin/ldconfig
%ldconfig_scriptlets -n libe1

%post -n libg1 -p /sbin/ldconfig
%postun -n libh1 -p /sbin/ldconfig
%post -n libi1 -p /sbin/ldconfig
%postun -n libi1
/sbin/ldconfig
/sbin/foo

%post -n libj1 -p /sbin/ldconfig
# keep both halves
%postun -n libj1 -p /sbin/ldconfig
%post -n libk1 -p /sbin/ldconfig
%if %{with bar}
%postun -n libk1 -p /sbin/ldconfig
%endif

%post -n libl1 -p /bin/bash
/sbin/ldconfig

%postun -n libl1 -p /sbin/ldconfig

%if %{with libs}
%ldconfig_scriptlets -n libn1
%ldconfig_scriptlets -n libo1

%if %{with alternatives}
%pre
/sbin/foo
%endif

%preun
/sbin/bar
%endif

%if %{with x}
%post -n libp1 -p /sbin/ldconfig
%else
%postun -n libp1 -p /sbin/ldconfig
%endif

%if 0%{?sle_version} && 0%{?sle_version} < 150400
%post -n libq1 -p /sbin/ldconfig
%postun -n libq1 -p /sbin/ldconfig
%else
%ldconfig_scriptlets -n libq1
%endif

%if %{with r}
%ldconfig_scriptlets -n libr1
%else
%ldconfig_scriptlets -n libr1-compat
%endif

%ldconfig_scriptlets -n libm1
# library files
%files -n libb1
%{_libdir}/libb.so.*

%changelog
