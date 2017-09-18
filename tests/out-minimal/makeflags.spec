%build
export CFLAGS="%{optflags}"
# make this easy
export CFLAGS="%{optflags} -blabla"
cd make
make
make PREFIX=/ \
     STATIC=""
make -j1

%changelog
