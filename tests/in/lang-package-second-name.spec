Name:           lang-package-second-name
Version:        1.0
Release:        0
Summary:        Test package
License:        MIT
URL:            https://example.org/lang-package-second-name

%description
Test package.

%package -n other
Summary:        Other package
Name:           other

%lang_package -n lang-package-second-name

%package -n other-lang
Summary:        Other lang package
Name:           other-lang
Recommends:     lang-package-second-name-lang

%changelog
