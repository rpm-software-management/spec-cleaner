Name: buildsuffix
#!BuildIgnore: foo [i586]
#!BuildIgnore: foo [i586]
#!BuildIgnore: bar baz
#!BuildConflicts: rpmlint-mini < 2.9 [x86_64,aarch64]
#!BuildConflicts: rpmlint-mini < 2.9 [x86_64,aarch64]
#!BuildConflicts: rpmlint-mini < 2.10 [x86_64,aarch64]
#!BuildConflicts: rpmlint-mini < 2.9 [i586]
#!BuildConflicts: libacl-devel pkg-config
# needed in the build root before anything else
#!BuildRequires: dupthing [i586]
# also stated by the bootstrap section below
#!BuildRequires: dupthing [i586]
BuildRequires: compiler
