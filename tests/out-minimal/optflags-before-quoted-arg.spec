%build
make CFLAGS="%{optflags}" "LIBDIR=%{_libdir}"
make OPT="%{optflags}" 'LDFLAGS=-lm'
./build.sh CFLAGS="%{optflags}" "$@"

%changelog
