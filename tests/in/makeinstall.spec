%install
rm -rf %{buildroot}
%makeinstall
%make_install
make install DESTDIR=%{buildroot}
make install DESTDIR=%{buildroot} -j1
make DESTDIR=%{buildroot} -j4 install
DESTDIR="%{buildroot}" make install
make DESTDIR=%{buildroot} install %{?_smp_mflags} \
