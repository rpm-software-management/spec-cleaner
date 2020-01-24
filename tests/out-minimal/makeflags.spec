%build
export CFLAGS="%{optflags}"
# make this easy
export CFLAGS="%{optflags} -blabla"
cd make
make
make PREFIX=/ \
     STATIC=""
make -j1
make %{?_smp_mflags} VERBOSE=1
make V=1 %{?_smp_mflags} all doc

%changelog
