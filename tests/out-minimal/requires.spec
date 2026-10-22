BuildRequires:  iii <= 4.2.1
BuildRequires:  jjj > %{version}
BuildRequires:  eee = %{version}-%{release}
BuildRequires:  bbb
BuildRequires:  aaa < 3.2.1
BuildRequires:  zzz
BuildRequires:  rrr >= %{version}
BuildRequires:  kkk
Requires:       iii <= 4.2.1
Requires:       jjj > %{version}
Requires:       eee = %{version}-%{release}
Requires:       bbb
Requires:       aaa < 3.2.1
Requires:       zzz
Requires:       pkgconfig(glib-2.0)
Requires:       perl(DBD::SQLite)
Requires:       rrr >= %{version}
Requires:       kkk
Requires:       %{some_packagename} >= %{some_version}
PreReq:         iii <= 4.2.1
PreReq:         jjj > %{version}
PreReq:         eee = %{version}-%{release}
PreReq:         aaa < 3.2.1
PreReq:         zzz
PreReq:         rrr >= %{version}
PreReq:         kkk
BuildRequires:  %{rubygem fast_gettext}
BuildRequires:  %{rubygem rails >= 3.2}
Requires:       php5 >= %{phpversion}
Provides:       locale(ru;bg)
Requires:       %{libname} >= %{version}
Requires:       pkgconfig(libcurl)
Provides:       %{name} = 0.3.0~gitbcaa
Obsoletes:      %{name} = 0.3.0~gitbcaa
Provides:       %{name} = 0.3.0+gitbcaa
Obsoletes:      %{name} = 0.3.0+gitbcaa
Requires:       alsa%{dep_postfix} >= 1.0.23
BuildRequires:  pkgconfig(yast2-core) >= 2.16.37
BuildRequires:  pkgconfig(yast2-ycp-ui-bindings) >= 2.16.37
BuildRequires:  alsa >= 1.0
BuildRequires:  alsa >= 1.3
BuildRequires:  alsa < 3.0
BuildRequires:  pkgconfig

%changelog
