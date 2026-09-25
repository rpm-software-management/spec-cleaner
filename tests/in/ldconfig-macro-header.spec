%install
make install

%post -n libfoo1 -p %run_ldconfig

%postun -n libfoo1 -p %{run_ldconfig}

%post
%run_ldconfig || :

%files
%{_libdir}/libfoo.so.1

%changelog
