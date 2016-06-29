%build
# not autoconf
CFLAGS="%{optflags} -fno-strict-aliasing" \
CXXFLAGS="%{optflags} -fno-strict-aliasing" \
./configure \
    --with-arguments

%changelog
