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
Requires:       curl
Recommends:     pattern() = yast_basis
Recommends:     wget

%package devel_gnome
%pattern_development
Summary:        GNOME Development
Group:          Metapackages
Provides:       pattern() = devel_gnome
Provides:       pattern-icon() = pattern-gnome-devel
# Don't freely assign order values, contact release managers
Provides:       pattern-order() = 3160
Provides:       pattern-visible()
Provides:       patterns-openSUSE-devel_gnome = %{version}
Obsoletes:      patterns-openSUSE-devel_gnome < %{version}
# SECTION PATTERNDATA
Requires:       pattern() = gnome_basis
Suggests:       pattern() = devel_C_C++
# /SECTION PATTERNDATA
Requires:       vim
Recommends:     gtk3
Suggests:       python-gobject

%changelog
