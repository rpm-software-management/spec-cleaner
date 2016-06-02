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

Requires:       %{libname} >= %{version} libcurl-devel
