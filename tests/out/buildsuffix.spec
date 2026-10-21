Name:           buildsuffix
BuildRequires:  compiler
# needed in the build root before anything else
# also stated by the bootstrap section below
#!BuildRequires: dupthing [i586]
BuildConflicts: pkg-config
BuildConflicts: pkgconfig(libacl)
#!BuildConflicts: rpmlint-mini < 2.10 [x86_64,aarch64]
#!BuildConflicts: rpmlint-mini < 2.9 [i586]
#!BuildConflicts: rpmlint-mini < 2.9 [x86_64,aarch64]
#!BuildIgnore:  bar
#!BuildIgnore:  baz
#!BuildIgnore:  foo [i586]

%changelog
