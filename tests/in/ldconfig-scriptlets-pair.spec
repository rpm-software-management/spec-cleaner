%install
make install

%post -n libs1 -p /sbin/ldconfig
%post -n libt1 -p /sbin/ldconfig

%preun
/sbin/baz

%postun -n libs1 -p /sbin/ldconfig
%postun -n libu1 -p /sbin/ldconfig

%preun -n libt1
/sbin/qux

%postun -n libt1 -p /sbin/ldconfig

%check
make check

%post -n %{name}%{sover} -p /sbin/ldconfig
%postun -n %{name}%{sover} -p /sbin/ldconfig

%post -n libtorch%{?pkg_suffix} -p /sbin/ldconfig
%postun -n libtorch%{?pkg_suffix} -p /sbin/ldconfig

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%postun -p /sbin/ldconfig -n libb1
%post -n libb1 -p /sbin/ldconfig

%if %{with foo}
%post -n libc1 -p /sbin/ldconfig
%postun -n libc1 -p /sbin/ldconfig
%endif

%post -n libd1 -p /sbin/ldconfig
%post -n libe1 -p /sbin/ldconfig
%postun -n libe1 -p /sbin/ldconfig

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
%post -n libn1 -p /sbin/ldconfig
%post -n libo1 -p /sbin/ldconfig

%if %{with alternatives}
%pre
/sbin/foo
%endif

%preun
/sbin/bar

%postun -n libn1 -p /sbin/ldconfig
%postun -n libo1 -p /sbin/ldconfig
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
%post -n libr1 -p /sbin/ldconfig
%postun -n libr1 -p /sbin/ldconfig
%else
%ldconfig_scriptlets -n libr1-compat
%endif

%post -n libm1 -p /sbin/ldconfig
%postun -n libm1 -p /sbin/ldconfig
# library files
%files -n libb1
%{_libdir}/libb.so.*

%changelog
