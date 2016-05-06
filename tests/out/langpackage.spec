%package -n something-lang
# FIXME: consider using %%lang_package macro
Summary:        Something
# FIXME: use correct group, see "https://en.opensuse.org/openSUSE:Package_group_guidelines"
Group:          Whatever

%package lang
# FIXME: consider using %%lang_package macro
Summary:        Something
# FIXME: use correct group, see "https://en.opensuse.org/openSUSE:Package_group_guidelines"
Group:          Whatever

%package lang
# I have reason not to convert this to lang macro
Summary:        Something
# FIXME: use correct group, see "https://en.opensuse.org/openSUSE:Package_group_guidelines"
Group:          Whatever

%package -n %{_name}
Summary:        Evolution Plugin for RSS Feeds Support
Group:          Productivity/Networking/Email/Clients
Recommends:     %{_name}-lang
Provides:       %{name} = %{version}

%changelog
