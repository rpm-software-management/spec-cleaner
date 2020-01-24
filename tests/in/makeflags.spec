%build
export CFLAGS=${RPM_OPT_FLAGS}
# make this easy
export CFLAGS="$RPM_OPT_FLAGS -blabla"
cd make
make
make PREFIX=/ \
     STATIC=""
make -j1
make %{?_smp_mflags} VERBOSE=1
make V=1 %{?_smp_mflags} all doc
