#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

BuildRequires:  aaa < 3.2.1
BuildRequires:  bbb
BuildRequires:  eee = %{version}
BuildRequires:  iii <= 4.2.1
BuildRequires:  jjj > %{version}
BuildRequires:  kkk
BuildRequires:  rrr >= %{version}
BuildRequires:  zzz

Requires:       aaa < 3.2.1
Requires:       bbb
Requires:       eee = %{version}
Requires:       iii <= 4.2.1
Requires:       jjj > %{version}
Requires:       kkk
Requires:       rrr >= %{version}
Requires:       zzz

Requires(pre):  aaa < 3.2.1
Requires(pre):  bbb
Requires(pre):  eee = %{version}
Requires(pre):  iii <= 4.2.1
Requires(pre):  jjj > %{version}
Requires(pre):  kkk
Requires(pre):  rrr >= %{version}
Requires(pre):  zzz
