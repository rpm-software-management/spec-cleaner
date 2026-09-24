Name:           langrecommendskeep
Version:        1.0
Release:        0
Summary:        Keep unrelated Recommends with %%lang_package
License:        MIT
Recommends:     %{name}-lang
Recommends:     someotherpackage

%description
Only the Recommends on the own lang subpackage is redundant with the
%%lang_package macro, unrelated Recommends lines must be kept.

%package -n %{name}-lang
Summary:        Translations for %{name}

%description -n %{name}-lang
Translations for %{name}.

%lang_package

%changelog
