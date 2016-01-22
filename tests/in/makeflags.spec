%build
export CFLAGS=${RPM_OPT_FLAGS}
export CFLAGS="$RPM_OPT_FLAGS -blabla"
make
make PREFIX=/ \
     STATIC=""
make -j1
