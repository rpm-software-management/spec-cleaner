# Dependency values the parser cannot split must be kept as they are
Requires:       %(rpm -q --queryformat '%{VERSION}' foo)
Name:           unparsable-dependencies
Version:        1
Release:        0
Summary:        Test
License:        MIT
BuildRequires:  foo # trailing comment
BuildRequires:  bar >=
BuildRequires:  pkg-config >= 2.2
Requires:       baz %{qux
Requires:       quux >= 1 < 2

%description
Test.

%files

%changelog
