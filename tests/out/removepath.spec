%package pool-openSUSE
Summary:        Chrony preconfiguration for openSUSE
Group:          Productivity/Networking/Other
Requires:       %{name} = %{version}
Conflicts:      %{name}-pool
Provides:       %{name}-pool = %{version}
Provides:       %{name}-pool-nonempty
RemovePathPostfixes: .opensuse
BuildArch:      noarch

%changelog
