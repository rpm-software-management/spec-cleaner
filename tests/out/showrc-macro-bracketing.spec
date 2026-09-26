# a macro rpm --showrc knows must not be braced inside a scriptlet section
Name:           showrc-macro-bracketing
Version:        1.0
Release:        0
Summary:        Test package
License:        MIT
URL:            https://example.org/showrc-macro-bracketing

%description
Test package.

%install
%cargo_install
%ldconfig_post

%files

%changelog
