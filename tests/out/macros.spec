%define useful_macro() ( echo 'Useful macro has been used with arg %{1}' )

%build
# FIXME: you should use %%cmake macros
cmake . \
	-DIHATECMAKE=OFF
# FIXME: you should use the %%configure macro
./configure --with-bells-and-whistles
# this is not autotools
./configure --aughr
%useful_macro 15
./configure.sh \

%changelog
