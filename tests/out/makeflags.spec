%build
export CFLAGS="%{optflags}"
export CFLAGS="%{optflags} -blabla"
make %{?_smp_mflags}
make PREFIX=/ \
     STATIC=""
make -j1

%changelog
