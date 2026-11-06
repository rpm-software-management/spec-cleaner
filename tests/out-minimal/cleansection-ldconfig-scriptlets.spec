%install
make install

%ldconfig_scriptlets -n libdemo1

%files
%{_bindir}/foo

%changelog
