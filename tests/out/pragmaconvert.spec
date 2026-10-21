Name:           pragmaconvert
Version:        1.0
BuildRequires:  %{base_name}-bootstrap
BuildRequires:  aaa
BuildRequires:  commented # why it is here
BuildRequires:  convertme
BuildRequires:  foo >= 1.2
# this one is needed by the build service only
BuildRequires:  glassfish-jaxb-runtime
BuildRequires:  multi1
BuildRequires:  multi2
BuildRequires:  pkgconfig
BuildRequires:  single
BuildRequires:  zsh
#!BuildRequires: (foo or bar)
#!BuildRequires: broken [x86_64] >= 1.0
#!BuildRequires: nospace[x86_64]
#!BuildRequires: projq [!home:proj]
#!BuildRequires: qualified [x86_64]
#!BuildRequires: qualonly [aarch64] # only there
#!BuildRequires: zeta [ppc64]
BuildConflicts: mixold # legacy combo
BuildConflicts: oldthing
BuildConflicts: rpmlint-mini < 2.9
#!BuildConflicts: mixq [i586]
#!BuildIgnore:  neverconvert
%if %{with bootstrap}
BuildRequires:  stringtemplate4-bootstrap
%else
BuildRequires:  stringtemplate4
%endif

%changelog
