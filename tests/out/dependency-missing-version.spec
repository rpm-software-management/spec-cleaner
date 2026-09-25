# A dependency operator without a version is kept as written
Name:           dependency-missing-version
Version:        1
Release:        0
Summary:        Test
License:        MIT
BuildRequires:  baz >=
Requires:       bar
Requires:       foo >,

%description
Test.

%files

%changelog
