%build
# local install
python scons/scons.py PREFIX=%{_prefix}/local
# more complicated case
python scons/scons.py PREFIX=%{_prefix}/lib/test/usr
# with spaces
python scons/scons.py PREFIX=%{_prefix} blah
# ending with newline
python scons/scons.py PREFIX=%{_prefix}
# just ending
python scons/scons.py PREFIX=%{_prefix}

%changelog
