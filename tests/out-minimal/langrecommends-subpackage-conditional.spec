Name:           langrecommends-subpackage-conditional
Version:        1.0
Release:        0
Summary:        Test package
License:        MIT
URL:            https://example.org/langrecommends-subpackage-conditional
%lang_package -n foo

%package -n foo
Summary:        The subpackage itself
%if 0%{?with_lang}
Recommends:     foo-lang
%endif

%description
Test package.

%changelog
