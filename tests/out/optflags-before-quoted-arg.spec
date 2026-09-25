%build
%make_build CFLAGS="%{optflags}" "LIBDIR=%{_libdir}"
%make_build OPT="%{optflags}" 'LDFLAGS=-lm'
./build.sh CFLAGS="%{optflags}" "$@"

%changelog
