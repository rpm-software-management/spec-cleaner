%install
install -D -m 0644 %{name}.conf %buildroot/etc/%{name}/%{name}.conf
mkdir -p %buildroot/var/lib/%{name}
