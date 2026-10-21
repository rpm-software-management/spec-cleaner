Name:           buildrequirespragma
BuildRequires:  %{base_name}-bootstrap
BuildRequires:  alib >= 1.2
# the build service needs the bootstrap tool in the build root first
BuildRequires:  antlr3-bootstrap-tool
BuildRequires:  compiler
BuildRequires:  pkgconfig
BuildRequires:  zlibrary-devel
#!BuildRequires: baz [!home:proj]
#!BuildRequires: foo [x86_64] bar [home:proj]

%changelog
