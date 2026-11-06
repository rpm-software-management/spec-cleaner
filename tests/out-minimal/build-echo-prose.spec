%build
echo "use cmake to build this package"
echo run ./configure now
echo done; cmake .
echo done && ./configure --prefix=/usr
./configure --prefix=/usr
cmake -DCMAKE_BUILD_TYPE=Release .
meson setup build
qmake-qt5 foo.pro
echo foo; echo cmake
echo hi && echo cmake .
echo ./configure --help; echo done

%changelog
