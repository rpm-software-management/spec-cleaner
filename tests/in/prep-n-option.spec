Name:           prep-n-option
Version:        1.0
Release:        0
Summary:        Test %prep with -n option
License:        MIT
URL:            https://example.org/
Patch1:         foo.patch

%description
Test that %prep -n foo is recognised as a section.

%prep -n foo-1.0
%patch1 -p1

%files
%{_bindir}/prep-n-option

%changelog
