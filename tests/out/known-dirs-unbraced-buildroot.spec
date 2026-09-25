%install
install -D -m 0644 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}

%changelog
