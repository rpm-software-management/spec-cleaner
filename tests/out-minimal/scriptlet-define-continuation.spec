# a backslash continued define inside %post must not be hoisted into the preamble
Name:           scriptlet-define-continuation
Version:        1.0
Release:        0
Summary:        Test package
License:        MIT
URL:            https://example.org/scriptlet-define-continuation

%description
Test package.

%post
echo before

%define _my_flag 1 \
    -o other
echo %{_my_flag}

%files

%changelog
