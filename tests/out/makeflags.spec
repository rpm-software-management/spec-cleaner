%build
export CFLAGS="%{optflags}"
# make this easy
export CFLAGS="%{optflags} -blabla"
cd make
make %{?_smp_mflags}
make PREFIX=/ \
     STATIC=""
make -j1

%changelog
