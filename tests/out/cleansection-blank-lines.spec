%install
mkdir -p %{buildroot}%{_datadir}/foo

%check
true

%files
%{_datadir}/foo

%files sub
%{_bindir}/sub

%files extra
%{_bindir}/extra

# kept above the next package
%files more
%{_bindir}/more

%changelog
