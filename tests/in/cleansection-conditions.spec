%install
make install

%clean
%if 0%{?suse_version} < 1200
rm -rf %{buildroot}
%endif

%files
%{_bindir}/main

%clean
rm -rf %{buildroot}
%if 0%{?suse_version} > 1500
%files sub
%{_bindir}/sub
%endif

%changelog
