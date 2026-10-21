Name:           pragmaconvert
Version:        1.0
BuildRequires:  aaa
BuildRequires:  zsh
#!BuildRequires: %{!?with_bootstrap:bootstrapthing}
#!BuildRequires: %{?with_x:condpkg}
#!BuildRequires: %{base_name}-bootstrap
#!BuildRequires: (foo or bar)
#!BuildRequires: broken [x86_64] >= 1.0
#!BuildRequires: commented # why it is here
#!BuildRequires: convertme zeta [ppc64]
#!BuildRequires: foo >= 1.2
# this one is needed by the build service only
#!BuildRequires: glassfish-jaxb-runtime
#!BuildRequires: multi1
#!BuildRequires: multi2
#!BuildRequires: nospace[x86_64]
#!BuildRequires: pkg-config
#!BuildRequires: plainmate
#!BuildRequires: projq [!home:proj]
#!BuildRequires: qualified [x86_64]
#!BuildRequires: qualonly [aarch64] # only there
#!BuildRequires: single
#!BuildConflicts: mixold mixq [i586] # legacy combo
#!BuildConflicts: oldthing
#!BuildConflicts: rpmlint-mini < 2.9
#!BuildIgnore:  neverconvert
%if %{with bootstrap}
#!BuildRequires: stringtemplate4-bootstrap
%else
#!BuildRequires: stringtemplate4
%endif

%changelog
