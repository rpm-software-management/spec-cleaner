%build
echo "use cmake to build this package"
echo run ./configure now
# FIXME: you should use the %%cmake macros
echo done; cmake .
# FIXME: you should use the %%configure macro
echo done && ./configure --prefix=%{_prefix}
# FIXME: you should use the %%configure macro
./configure --prefix=%{_prefix}
# FIXME: you should use the %%cmake macros
cmake -DCMAKE_BUILD_TYPE=Release .
# FIXME: you should use the %%meson macros
meson setup build
# FIXME: you should use the %%qmake5 macro
qmake-qt5 foo.pro

%changelog
