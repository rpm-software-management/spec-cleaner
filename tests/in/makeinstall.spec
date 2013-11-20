%install
rm -rf %{buildroot}
%makeinstall
%make_install
make install DESTDIR=%{buildroot}
