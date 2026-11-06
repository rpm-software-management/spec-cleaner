Name:           provides-unversioned
Version:        1.0
Release:        0
Summary:        Keep unversioned Provides/Obsoletes/Conflicts
License:        MIT
URL:            https://example.com
Provides:       foo
Provides:       foo = 1.0
Obsoletes:      bar
Obsoletes:      bar < 2.0
Conflicts:      baz < 2.0
Conflicts:      baz
Conflicts:      quux
Conflicts:      quux < 2.0
Requires:       qux
Requires:       qux >= 1.0

%description
An unversioned Provides/Obsoletes/Conflicts covers every version, so it must
not be dropped when a versioned entry for the same name exists.

%changelog
