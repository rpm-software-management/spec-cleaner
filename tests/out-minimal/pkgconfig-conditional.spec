Name:           pkgconfig-conditional
Version:        1.0
Release:        0
Summary:        Conditional pkgconfig declarations and statements
License:        MIT
BuildRequires:  pkgconfig(474module)
BuildRequires:  pkgconfig
%if 1
BuildRequires:  pkgconfig
%endif
%if 1
BuildRequires:  pkgconfig(474conditional)
%endif

%description
The unconditional pkgconfig() dependency has no unconditional
declaration - the only one sits inside a conditional block, which the
cleaner does not credit - so the declaration is inserted. The
conditional statement alone would not trigger an insertion.

%changelog
