%package dhcp_dns_server
%pattern_serverfunctions
Summary:        DHCP and DNS Server
Group:          Metapackages
Provides:       pattern() = dhcp_dns_server
Provides:       pattern-icon() = yast-dns-server
Provides:       pattern-order() = 3040
Provides:       pattern-visible()
Provides:       patterns-openSUSE-dhcp_dns_server = %{version}
Obsoletes:      patterns-openSUSE-dhcp_dns_server < %{version}
Requires:       pattern() = basesystem
