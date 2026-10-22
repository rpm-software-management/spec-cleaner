Name:           buildrequirespragma
BuildRequires:  compiler
# the build service needs the bootstrap tool in the build root first
#!BuildRequires: antlr3-bootstrap-tool
#!BuildRequires: zlibrary-devel
#!BuildRequires: alib >= 1.2
#!BuildRequires: pkg-config
#!BuildRequires: %{base_name}-bootstrap
#!BuildRequires: foo [x86_64] bar [home:proj]
#!BuildRequires: baz [!home:proj]

%changelog
