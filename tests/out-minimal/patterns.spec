%package dhcp_dns_server
Summary:        DHCP and DNS Server
Group:          Metapackages
Requires:       pattern() = basesystem
Provides:       pattern() = dhcp_dns_server
Provides:       pattern-icon() = yast-dns-server
Provides:       pattern-order() = 3040
Provides:       pattern-visible()
Provides:       patterns-openSUSE-dhcp_dns_server = %{version}
Obsoletes:      patterns-openSUSE-dhcp_dns_server < %{version}
%pattern_serverfunctions

%changelog
