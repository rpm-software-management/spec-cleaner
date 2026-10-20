Name: buildsuffix
#!BuildIgnore: foo [i586]
#!BuildIgnore: bar baz
#!BuildConflicts: rpmlint-mini < 2.9 [x86_64,aarch64]
#!BuildConflicts: libacl-devel pkg-config
BuildRequires: compiler
