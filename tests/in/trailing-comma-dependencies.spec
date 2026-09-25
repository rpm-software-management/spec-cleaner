# Extra separators after a versioned dependency must not produce an empty dependency
Name:           trailing-comma-dependencies
Version:        1
Release:        0
Summary:        Test
License:        MIT
BuildRequires:  qux >= 2,
Requires:       bar, foo >= 1.0,
Requires:       baz = 3,, quux

%description
Test.

%files

%changelog
