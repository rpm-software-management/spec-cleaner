%build
# local install
python scons/scons.py PREFIX=/usr/local
# more complicated case
python scons/scons.py PREFIX=/usr/libexec/test/usr
# with spaces
python scons/scons.py PREFIX=/usr blah
# ending with newline
python scons/scons.py PREFIX=/usr
# just ending
python scons/scons.py PREFIX=/usr
