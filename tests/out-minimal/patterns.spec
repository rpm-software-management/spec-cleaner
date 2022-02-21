%package dhcp_dns_server
%pattern_serverfunctions
Summary:        DHCP and DNS Server
Group:          Metapackages
Provides:       pattern() = dhcp_dns_server
Provides:       pattern-icon() = yast-dns-server
Provides:       pattern-order() = 3040
Provides:       pattern-visible()
Requires:       pattern() = basesystem
Recommends:     pattern() = yast_basis
Provides:       patterns-openSUSE-dhcp_dns_server = %{version}
Obsoletes:      patterns-openSUSE-dhcp_dns_server < %{version}
Requires:       curl
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

%package base
%pattern_basetechnologies
Summary:        Base System
Group:          Metapackages
Provides:       pattern() = base
Provides:       pattern-icon() = pattern-basis
Provides:       pattern-order() = 1030
Provides:       pattern-visible()
Requires:       pattern() = minimal_base
Recommends:     pattern() = basesystem
Suggests:       pattern() = yast_basis
Requires:       aaa_base
Requires:       bash
Requires:       ca-certificates-mozilla
Requires:       coreutils
Requires:       glibc
Requires:       libnss_usrfiles2
Requires:       pam
Requires:       pam-config
# Support multiversion(kernel) (jsc#SLE-10162)
Requires:       purge-kernels-service
Requires:       rpm
Requires:       system-user-nobody
Requires:       util-linux
# Add some static base tool in case system explodes; Recommend only, as users are free to uninstall it
Recommends:     busybox-static
Recommends:     haveged
%obsolete_legacy_pattern base
%{obsolete_legacy_pattern minimal}

%changelog
