Name:           langrecommends-main-named
Version:        1.0
Release:        0
Summary:        Drop Recommends on the lang package named after the main package
License:        MIT

%description
The %%lang_package -n macro named after the main package generates its own
lang package, so the Recommends on it is redundant in any spelling.

%lang_package -n langrecommends-main-named

%changelog
