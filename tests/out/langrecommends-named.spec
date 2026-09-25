%define _name evolution-rss
Name:           evolution-plugin-rss
Version:        1.0
Release:        0
Summary:        Drop Recommends on the lang package named by %%lang_package -n
License:        MIT
Recommends:     %{name}-lang

%description
The %%lang_package -n macro generates %%{_name}-lang, so only the Recommends
on it is redundant, the one on %%{name}-lang must be kept.

%package -n %{_name}
Summary:        RSS reader

%description -n %{_name}
RSS reader.

%lang_package -n %{_name}

%changelog
