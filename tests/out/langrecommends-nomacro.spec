Name:           langrecommends-nomacro
Version:        1.0
Release:        0
Summary:        Keep Recommends on hand-rolled lang subpackage
License:        MIT
Recommends:     %{name}-lang

%description
The lang subpackage is hand-rolled without the %%lang_package macro (like
vlc), so the Recommends must stay to pull it in.

%package -n %{name}-lang
# Hand-rolled translations package, deliberately not using %%lang_package
Summary:        Translations for %{name}

%description -n %{name}-lang
Translations for %{name}.

%files -n %{name}-lang

%changelog
