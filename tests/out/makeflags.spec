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
%make_build
%make_build PREFIX=/ \
     STATIC=""
%make_build -j1
%make_build
%make_build all doc

%changelog
