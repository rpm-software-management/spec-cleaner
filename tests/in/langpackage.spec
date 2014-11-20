%package -n something-lang
Summary:        Something
Group:          Whatever

%package lang
Summary:        Something
Group:          Whatever

%package lang
# I have reason not to convert this to lang macro
Summary:        Something
Group:          Whatever

%package -n %{_name}
Summary:        Evolution Plugin for RSS Feeds Support
Group:          Productivity/Networking/Email/Clients
Recommends:     %{_name}-lang
Provides:       %{name} = %{version}
