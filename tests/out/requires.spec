BuildRequires:  %{rubygem fast_gettext}
BuildRequires:  %{rubygem rails >= 3.2}
BuildRequires:  aaa < 3.2.1
BuildRequires:  alsa < 3.0
BuildRequires:  alsa >= 1.0
BuildRequires:  alsa >= 1.3
BuildRequires:  bbb
BuildRequires:  eee = %{version}-%{release}
BuildRequires:  iii <= 4.2.1
BuildRequires:  jjj > %{version}
BuildRequires:  kkk
BuildRequires:  pkgconfig
BuildRequires:  rrr >= %{version}
BuildRequires:  zzz
BuildRequires:  pkgconfig(yast2-core) >= 2.16.37
BuildRequires:  pkgconfig(yast2-ycp-ui-bindings) >= 2.16.37
Requires:       %{libname} >= %{version}
Requires:       %{some_packagename} >= %{some_version}
Requires:       aaa < 3.2.1
Requires:       alsa%{dep_postfix} >= 1.0.23
Requires:       bbb
Requires:       eee = %{version}-%{release}
Requires:       iii <= 4.2.1
Requires:       jjj > %{version}
Requires:       kkk
Requires:       php5 >= %{phpversion}
Requires:       rrr >= %{version}
Requires:       zzz
Requires:       perl(DBD::SQLite)
Requires:       pkgconfig(glib-2.0)
Requires:       pkgconfig(libcurl)
# FIXME: use proper Requires(pre/post/preun/...)
PreReq:         aaa < 3.2.1
PreReq:         eee = %{version}-%{release}
PreReq:         iii <= 4.2.1
PreReq:         jjj > %{version}
PreReq:         kkk
PreReq:         rrr >= %{version}
PreReq:         zzz
Provides:       locale(ru;bg)
Provides:       %{name} = 0.3.0~gitbcaa
Obsoletes:      %{name} = 0.3.0~gitbcaa
Provides:       %{name} = 0.3.0+gitbcaa
Obsoletes:      %{name} = 0.3.0+gitbcaa

%changelog
