%build
%{?suse_update_config:%{suse_update_config -f}}
%{suse_update_config -f}
%suse_update_config -f
cmake . \
	-DIHATECMAKE=OFF
./configure --with-bells-and-whistles
# this is not autotools
./configure --aughr
