%install
%makeinstall
%make_install
make install DESTDIR=%{buildroot}
make install DESTDIR=%{buildroot}
make install DESTDIR=%{buildroot} -j1
make DESTDIR=%{buildroot} -j4 install
$RPM_BUILD_ROOT_REPLACEMENT != %{buildroot} == %{buildroot} == %{buildroot}
DESTDIR=%{buildroot} make install
make %{?_smp_mflags} DESTDIR=%{buildroot} install \

%changelog
