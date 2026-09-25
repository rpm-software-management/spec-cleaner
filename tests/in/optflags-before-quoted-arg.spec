%build
make CFLAGS=$RPM_OPT_FLAGS "LIBDIR=%{_libdir}"
make OPT=${RPM_OPT_FLAGS} 'LDFLAGS=-lm'
./build.sh CFLAGS=$RPM_OPT_FLAGS "$@"
