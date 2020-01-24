%build
export CFLAGS="%{optflags}"
# make this easy
export CFLAGS="%{optflags} -blabla"
cd make
%make_build
%make_build PREFIX=/ \
     STATIC=""
%make_build -j1
%make_build
%make_build all doc

%changelog
