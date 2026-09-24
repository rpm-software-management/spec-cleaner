Name:           langrecommendsliteral
Version:        1.0
Release:        0
Summary:        Drop redundant literal Recommends on the lang subpackage
License:        MIT

%description
The literal Recommends on the lang subpackage is redundant when the
%%lang_package macro is used as it generates Supplements for it.

%package -n langrecommendsliteral-lang
Summary:        Translations for langrecommendsliteral

%description -n langrecommendsliteral-lang
Translations for langrecommendsliteral.

%lang_package

%changelog
