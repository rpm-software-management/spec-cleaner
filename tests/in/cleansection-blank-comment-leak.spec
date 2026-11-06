%install
make install

%clean
rm -rf %{buildroot}

# remove also the temp dir
rm -rf /tmp/cleanleak

%files
%{_bindir}/foo
