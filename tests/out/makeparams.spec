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
%make_install install-etc
%make_install
%make_install
%make_install
%make_install
%make_install
%make_install
%make_install
%make_install
%make_install
%make_install
%make_install
%make_install
%make_install
%make_install
%make_install
%make_install
%make_install
%make_install
%make_install
%make_install
%make_install
%make_install
%make_install
%make_install
%make_install
%make_install
%make_install

%changelog
