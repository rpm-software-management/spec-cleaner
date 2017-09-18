%build
export CFLAGS=${RPM_OPT_FLAGS}
# make this easy
export CFLAGS="$RPM_OPT_FLAGS -blabla"
cd make
make
make PREFIX=/ \
     STATIC=""
make -j1
