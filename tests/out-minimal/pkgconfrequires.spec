%if %{with curses}
BuildRequires:  pkgconfig(ncurses)
%endif
BuildRequires:  pkgconfig(blabla)
BuildRequires:  pkgconfig >= 2.2
Requires:       pkgconfig(blabla)

%changelog
