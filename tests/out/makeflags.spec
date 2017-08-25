%build
export CFLAGS="%{optflags}"
# make this easy
export CFLAGS="%{optflags} -blabla"
make %{?_smp_mflags}
make PREFIX=/ \
     STATIC=""
make -j1

%changelog
