%check
make %{?_smp_mflags} V=1 check RUNTEST=true
make -j1 check
make %{?_smp_mflags} test V=1

%changelog
