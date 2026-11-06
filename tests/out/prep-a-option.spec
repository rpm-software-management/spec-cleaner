Name:           prep-a-option
Version:        1.0
Release:        0
Summary:        Test %prep with -a option
License:        MIT
URL:            https://example.org/
Patch1:         foo.patch

%description
Test that %prep -a is recognised as a section.

%prep
%autosetup -p1

%prep -a
echo extra prep step

%files
%{_bindir}/prep-a-option

%changelog
