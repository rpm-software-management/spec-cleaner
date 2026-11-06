%install
make install

%clean
rm -rf %{buildroot}

%ldconfig_scriptlets -n libdemo1

%files
%{_bindir}/foo
