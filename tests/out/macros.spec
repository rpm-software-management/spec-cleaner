%define _prefix=/opt/kde3
%define useful_macro() ( echo 'Useful macro has been used with arg %{1}' )

%build
# FIXME: you should use the %%cmake macros
cmake . \
	-DIHATECMAKE=OFF
# FIXME: you should use the %%configure macro
./configure --with-bells-and-whistles
# this is not autotools
./configure --aughr
%useful_macro 15
./configure.sh \

# FIXME: you should use the %%configure macro
CFLAGS="%{optflags} -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -fPIE" \
LDFLAGS="-pie" \
./configure \

# FIXME: you should use the %%configure macro
CFLAGS="-g" ./configure

# FIXME: you should use the %%qmake5 macro
qmake-qt5 %{name}.pro -spec linux-g++

# FIXME: you should use the %%meson macros
meson

# we are doing stuff with cmake and should not add fixme above this comment

%changelog
