%build
export CFLAGS="%{optflags}"
# make this easy
export CFLAGS="%{optflags} -blabla"
CFLAGS="%{optflags}" python3 setup.py build
export CFLAGS="%{optflags}" CXXFLAGS="%{optflags}"
sed -i "s/^CFLAGS=/CFLAGS=%{optflags} /" Makefile
export CFLAGS="${RPM_OPT_FLAGS/-fstack-protector-strong/}"
install -d ${RPM_BUILD_ROOT%/}/foo
cd make
make
make PREFIX=/ \
     STATIC=""
make -j1
make %{?_smp_mflags} VERBOSE=1
make V=1 %{?_smp_mflags} all doc

%changelog
