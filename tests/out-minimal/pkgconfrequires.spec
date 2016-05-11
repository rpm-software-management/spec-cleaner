BuildRequires:  pkgconfig >= 2.2
BuildRequires:  pkgconfig(blabla)
Requires:       pkgconfig
Requires:       pkgconfig(blabla)
%if %{with curses}
BuildRequires:  pkgconfig(ncurses)
%endif

%changelog
