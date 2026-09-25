Name:           langrecommends-minimal
Version:        1.0
Release:        0
Summary:        Keep Recommends on the lang subpackage in minimal mode
License:        MIT
# translations are useful
Recommends:     %{name}-lang
Recommends:     someotherpackage

%description
Minimal mode keeps the Recommends on the lang subpackage and its comment,
even with the %%lang_package macro.

%lang_package

%changelog
