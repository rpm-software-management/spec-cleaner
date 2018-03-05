%package dhcp_dns_server
%pattern_serverfunctions
Summary:        DHCP and DNS Server
Group:          Metapackages
Provides:       pattern-icon() = yast-dns-server
Provides:       pattern-visible()
Provides:       pattern() = dhcp_dns_server
Provides:       patterns-openSUSE-dhcp_dns_server = %{version}
Obsoletes:      patterns-openSUSE-dhcp_dns_server < %{version}
Requires:       pattern() = basesystem
Recommends:     pattern() = yast_basis
Provides:       pattern-order() = 3040
Requires:       curl
Recommends:     wget
