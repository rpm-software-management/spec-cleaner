%transfiletriggerin -- %{_libdir}
/sbin/ldconfig

%filetriggerun -n libfoo -- %{_libdir}
/sbin/ldconfig

%post -p /bin/bash
/sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/libfoo.so.1

%changelog
