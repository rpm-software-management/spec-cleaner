%install
rm -rf %{buildroot}
%makeinstall
%make_install
make install DESTDIR=%{buildroot}
make DESTDIR=%{buildroot} -j4 install
DESTDIR="%{buildroot}" make install
