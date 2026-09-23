Name:           langrecommends
Version:        1.0
Release:        0
Summary:        Drop redundant Recommends on the lang subpackage
License:        MIT

%description
The Recommends on the lang subpackage is redundant when the %%lang_package
macro is used as it generates Supplements for it.

%package -n %{name}-lang
Summary:        Translations for %{name}

%description -n %{name}-lang
Translations for %{name}.

%lang_package

%changelog
