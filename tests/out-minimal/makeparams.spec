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
make check ||:
make && mv mtr xmtr
make %{?_smp_mflags} VERBOSE=1

%install
%makeinstall install-etc
make DESTDIR=%{buildroot} install
make DESTDIR=%buildroot install
make DESTDIR=%{buildroot} install
make DESTDIR=%buildroot install
make DESTDIR=%{buildroot} install
make DESTDIR=%buildroot install
make DESTDIR=%{buildroot} install
make DESTDIR=%{buildroot} install
make DESTDIR=%{buildroot} install
make DESTDIR=%{buildroot} install
make DESTDIR=%{buildroot} install
make DESTDIR=%{buildroot} install
make install DESTDIR=%buildroot
make install DESTDIR=%{buildroot}
make install DESTDIR=%buildroot
make install DESTDIR=%{buildroot}
make install DESTDIR=%buildroot
make install DESTDIR=%{buildroot}
make install DESTDIR=%{buildroot}
make install DESTDIR=%{buildroot}
make install DESTDIR=%{buildroot}
make install DESTDIR=%{buildroot}
make install DESTDIR=%{buildroot}
make install DESTDIR=%{buildroot}
%make_install
%{make_install}
make install  %{?_smp_mflags}

%changelog
