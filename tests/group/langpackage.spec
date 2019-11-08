%package -n something-lang
# FIXME: consider using %%lang_package macro
Summary:        Something

%package lang
# FIXME: consider using %%lang_package macro
Summary:        Something

%package lang
# I have reason not to convert this to lang macro
Summary:        Something

%package -n %{_name}
Summary:        Evolution Plugin for RSS Feeds Support
Recommends:     %{_name}-lang
Provides:       %{name} = %{version}

%changelog
