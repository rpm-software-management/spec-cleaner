%build
make
make PREFIX=/ \
     STATIC=""
make -j1
