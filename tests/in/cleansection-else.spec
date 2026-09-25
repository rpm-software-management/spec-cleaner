%install
make install

%clean
%if 0%{?suse_version}
rm -rf %{buildroot}
%else
%files
%{_bindir}/main
%endif

%changelog
