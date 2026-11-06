%install
make install

%clean
rm -rf %{buildroot}

# keep this note

%if 0%{?suse_version}
%files
%{_bindir}/foo
%endif
