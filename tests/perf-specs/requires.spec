BuildRequires: iii  <=     4.2.1 jjj>  %{version} eee=%{version}-%{release} bbb
BuildRequires:      aaa<3.2.1 zzz
BuildRequires:    rrr >= %{version} kkk

Requires: iii  <=     4.2.1 jjj>  %{version} eee=%{version}-%{release} bbb
Requires:      aaa<3.2.1 zzz     pkgconfig(glib-2.0) perl(DBD::SQLite)
Requires:    rrr >= %{version} kkk
Requires:     %{some_packagename} => %{some_version}

PreReq: iii  <=     4.2.1 jjj>  %{version} eee=%{version}-%{release} aaa
PreReq:      aaa<3.2.1 zzz
PreReq:    rrr >= %{version} kkk

BuildRequires:  %{rubygem fast_gettext}
BuildRequires:  %{rubygem rails >= 3.2}

Requires: php5 => %{phpversion}
Provides:       locale(ru;bg)
Requires:       %{libname} >= %{version} libcurl-devel
Provides:       %{name} = 0.3.0~gitbcaa
Obsoletes:      %{name} = 0.3.0~gitbcaa
Provides:       %{name} = 0.3.0+gitbcaa
Obsoletes:      %{name} = 0.3.0+gitbcaa
Requires:       alsa%{dep_postfix} >= 1.0.23

BuildRequires:  yast2-core-devel
BuildRequires:  yast2-core-devel >= 2.16.37
BuildRequires:  yast2-ycp-ui-bindings-devel
BuildRequires:  yast2-ycp-ui-bindings-devel >= 2.16.37
BuildRequires:  alsa >= 1.0
BuildRequires:  alsa >= 1.3
BuildRequires:  alsa < 3.0
