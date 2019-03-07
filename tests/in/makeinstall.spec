%install
rm -rf %{buildroot}
%makeinstall
%make_install
make %{?_smp_mflags} DESTDIR=%{buildroot} install \
make install DESTDIR="$RPM_BUILD_ROOT"
make install DESTDIR=%{buildroot}
make install DESTDIR=%{buildroot} -j1
make DESTDIR=%{buildroot} -j4 install
$RPM_BUILD_ROOT_REPLACEMENT != $RPM_BUILD_ROOT == ${RPM_BUILD_ROOT} == $RPM_BUILD_ROOT
DESTDIR="%{buildroot}" make install
