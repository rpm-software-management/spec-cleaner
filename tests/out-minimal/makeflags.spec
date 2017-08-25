%build
export CFLAGS="%{optflags}"
# make this easy
export CFLAGS="%{optflags} -blabla"
make
make PREFIX=/ \
     STATIC=""
make -j1

%changelog
