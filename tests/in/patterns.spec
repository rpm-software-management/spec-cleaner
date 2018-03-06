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

%package devel_gnome
%pattern_development
Summary:        GNOME Development
Group:          Metapackages
Recommends:     gtk3

Provides:       pattern() = devel_gnome
Provides:       pattern-icon() = pattern-gnome-devel
# Don't freely assign order values, contact release managers
Provides:       pattern-order() = 3160
Provides:       pattern-visible()
# SECTION PATTERNDATA
Suggests:       pattern() = devel_C_C++
Requires:       pattern() = gnome_basis
# /SECTION PATTERNDATA
Provides:       patterns-openSUSE-devel_gnome = %{version}
Obsoletes:      patterns-openSUSE-devel_gnome < %{version}
Suggests:       python-gobject
Requires:       vim
