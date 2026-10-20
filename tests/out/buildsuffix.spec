Name:           buildsuffix
BuildRequires:  compiler
#!BuildConflicts: libacl-devel
#!BuildConflicts: pkg-config
#!BuildConflicts: rpmlint-mini < 2.9 [x86_64,aarch64]
#!BuildIgnore:  bar
#!BuildIgnore:  baz
#!BuildIgnore:  foo [i586]

%changelog
