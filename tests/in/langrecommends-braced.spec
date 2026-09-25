Name:           langrecommends-braced
Version:        1.0
Release:        0
Summary:        Drop redundant Recommends with the braced lang_package macro
License:        MIT
Recommends:     %{name}-lang

%description
The braced %%{lang_package} macro generates Supplements for the lang
subpackage as well, so the Recommends on it is redundant.

%{lang_package}

%changelog
