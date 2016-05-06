%build
make %{?_smp_mflags}
make %{?_smp_mflags}
make %{?_smp_mflags}
make %{?_smp_mflags}
make %{?_smp_mflags}
make %{?_smp_mflags}
make %{?_smp_mflags}
make %{?_smp_mflags}
make %{?_smp_mflags}
make %{?_smp_mflags}
make %{?_smp_mflags}
make %{?_smp_mflags}
make %{?_smp_mflags}
make %{?_smp_mflags}
make %{?_smp_mflags}
make %{?_smp_mflags}
make %{?_smp_mflags}
make %{?_smp_mflags}
make %{?_smp_mflags}
make %{?_smp_mflags}
make %{?_smp_mflags}
make %{?_smp_mflags}
make %{?_smp_mflags}
make %{?_smp_mflags}
make %{?_smp_mflags}
make %{?_smp_mflags}
make %{?_smp_mflags}
make %{?_smp_mflags} check ||:
make %{?_smp_mflags} && mv mtr xmtr
make %{?_smp_mflags} VERBOSE=1

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install install-etc
make %{?_smp_mflags} DESTDIR=%{buildroot} install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
%make_install
%make_install
make %{?_smp_mflags} DESTDIR=%{buildroot} install

%changelog
