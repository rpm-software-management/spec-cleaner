Name:           buildsuffix
#!BuildIgnore:  foo [i586]
#!BuildIgnore:  bar
#!BuildIgnore:  baz
#!BuildConflicts: rpmlint-mini < 2.9 [x86_64,aarch64]
#!BuildConflicts: rpmlint-mini < 2.10 [x86_64,aarch64]
#!BuildConflicts: rpmlint-mini < 2.9 [i586]
#!BuildConflicts: libacl-devel
#!BuildConflicts: pkg-config
# needed in the build root before anything else
# also stated by the bootstrap section below
#!BuildRequires: dupthing [i586]
BuildRequires:  compiler

%changelog
