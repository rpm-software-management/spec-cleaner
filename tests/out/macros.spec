%build
# FIXME: you should use %%cmake macros
cmake . \
	-DIHATECMAKE=OFF
# FIXME: you should use the %%configure macro
./configure --with-bells-and-whistles
# this is not autotools
./configure --aughr

%changelog
