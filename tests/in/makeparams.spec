%build
%__make %{?jobs: -j%jobs}
%__make %{?jobs:-j %jobs}
%__make %{?jobs:-j%jobs}
%{__make} %{?jobs: -j%jobs}
%{__make} %{?jobs:-j %jobs}
%{__make} %{?jobs:-j%jobs}
make %{?jobs: -j%jobs}
make %{?jobs:-j %jobs}
make %{?jobs:-j%jobs}
%__make %{?jobs: -j%{jobs}}
%__make %{?jobs:-j %{jobs}}
%__make %{?jobs:-j%{jobs}}
%{__make} %{?jobs: -j%{jobs}}
%{__make} %{?jobs:-j %{jobs}}
%{__make} %{?jobs:-j%{jobs}}
make %{?jobs: -j%{jobs}}
make %{?jobs:-j %{jobs}}
make %{?jobs:-j%{jobs}}
%__make %_smp_mflags
%__make %{_smp_mflags}
%__make %{?_smp_mflags}
%{__make} %_smp_mflags
%{__make} %{_smp_mflags}
%{__make} %{?_smp_mflags}
make %_smp_mflags
make %{_smp_mflags}
make %{?_smp_mflags}
make check ||:
make && mv mtr xmtr
make %{?_smp_flags} VERBOSE=1

%install
%makeinstall install-etc
%__make DESTDIR=%{buildroot} install
%__make DESTDIR=%buildroot install
%{__make} DESTDIR=%{buildroot} install
%{__make} DESTDIR=%buildroot install
make DESTDIR=%{buildroot} install
make DESTDIR=%buildroot install
%__make DESTDIR=${RPM_BUILD_ROOT} install
%__make DESTDIR=$RPM_BUILD_ROOT install
%{__make} DESTDIR=${RPM_BUILD_ROOT} install
%{__make} DESTDIR=$RPM_BUILD_ROOT install
make DESTDIR=${RPM_BUILD_ROOT} install
make DESTDIR=$RPM_BUILD_ROOT install
%__make install DESTDIR=%buildroot
%__make install DESTDIR=%{buildroot}
%{__make} install DESTDIR=%buildroot
%{__make} install DESTDIR=%{buildroot}
make install DESTDIR=%buildroot
make install DESTDIR=%{buildroot}
%__make install DESTDIR=${RPM_BUILD_ROOT}
%__make install DESTDIR=$RPM_BUILD_ROOT
%{__make} install DESTDIR=${RPM_BUILD_ROOT}
%{__make} install DESTDIR=$RPM_BUILD_ROOT
make install DESTDIR=${RPM_BUILD_ROOT}
make install DESTDIR=$RPM_BUILD_ROOT
%make_install
%{make_install}
%{__make} install %{?jobs:-j%{jobs}}
