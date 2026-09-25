%build
export CFLAGS=${RPM_OPT_FLAGS}
# make this easy
export CFLAGS="$RPM_OPT_FLAGS -blabla"
CFLAGS=$RPM_OPT_FLAGS python3 setup.py build
export CFLAGS=$RPM_OPT_FLAGS CXXFLAGS=$RPM_OPT_FLAGS
sed -i "s/^CFLAGS=/CFLAGS=$RPM_OPT_FLAGS /" Makefile
export CFLAGS="${RPM_OPT_FLAGS/-fstack-protector-strong/}"
install -d ${RPM_BUILD_ROOT%/}/foo
cd make
make
make PREFIX=/ \
     STATIC=""
make -j1
make %{?_smp_mflags} VERBOSE=1
make V=1 %{?_smp_mflags} all doc
