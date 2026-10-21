Name: pragmaconvert
Version: 1.0
BuildRequires: zsh
#!BuildRequires:  single
# this one is needed by the build service only
#!BuildRequires:  glassfish-jaxb-runtime
#!BuildRequires:  multi1 multi2
#!BuildRequires:  foo >= 1.2
#!BuildRequires:  %{base_name}-bootstrap
#!BuildRequires:  pkg-config
#!BuildRequires:  qualified [x86_64]
#!BuildRequires:  projq [!home:proj]
#!BuildRequires:  convertme zeta [ppc64]
#!BuildRequires:  (foo or bar)
#!BuildRequires:  commented # why it is here
#!BuildRequires:  qualonly [aarch64] # only there
#!BuildConflicts:  oldthing
#!BuildConflicts:  rpmlint-mini < 2.9
#!BuildConflicts:  mixold mixq [i586] # legacy combo
#!BuildRequires:  broken [x86_64] >= 1.0
#!BuildRequires:  nospace[x86_64]
#!BuildRequires:  %{?with_x:condpkg} plainmate
#!BuildRequires:  %{!?with_bootstrap:bootstrapthing}
#!BuildIgnore:  neverconvert
%if %{with bootstrap}
#!BuildRequires:  stringtemplate4-bootstrap
%else
#!BuildRequires:  stringtemplate4
%endif
BuildRequires: aaa
