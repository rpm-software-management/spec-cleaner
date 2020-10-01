%package pool-openSUSE
Summary:        Chrony preconfiguration for openSUSE
Group:          Productivity/Networking/Other
Provides:       %name-pool = %version
Provides:       %name-pool-nonempty
Conflicts:      otherproviders(%name-pool)
Requires:       %name = %version
BuildArch:      noarch
RemovePathPostfixes: .opensuse
