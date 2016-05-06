%build
export CFLAGS="%{optflags}"
export CFLAGS="%{optflags} -blabla"
make
make PREFIX=/ \
     STATIC=""
make -j1

%changelog
