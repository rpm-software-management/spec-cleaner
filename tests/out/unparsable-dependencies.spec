# Dependency values the parser cannot split must be kept as they are
Name:           unparsable-dependencies
Version:        1
Release:        0
Summary:        Test
License:        MIT
BuildRequires:  bar >=
BuildRequires:  foo # trailing comment
BuildRequires:  pkgconfig >= 2.2
# FIXME: Use %requires_eq macro instead
Requires:       %(rpm -q --queryformat '%{VERSION}' foo)
Requires:       baz %{qux
Requires:       quux >= 1 < 2

%description
Test.

%files

%changelog
