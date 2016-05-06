%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
%make_install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
make -j1 DESTDIR=%{buildroot} install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
$RPM_BUILD_ROOT_REPLACEMENT != %{buildroot} == %{buildroot} == %{buildroot}
make %{?_smp_mflags} DESTDIR=%{buildroot} install
make %{?_smp_mflags} DESTDIR=%{buildroot} install \

%changelog
