%install
make install

%clean
rm -rf %{buildroot}

# keep this note about files

%files
%{_bindir}/foo
