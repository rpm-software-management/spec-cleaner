%build
echo "use cmake to build this package"
echo run ./configure now
./configure --prefix=/usr
cmake -DCMAKE_BUILD_TYPE=Release .
meson setup build
qmake-qt5 foo.pro

%changelog
