#
# spec file for package requires
#
# Copyright (c) 2013 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


BuildRequires:  %{rubygem fast_gettext}
BuildRequires:  %{rubygem rails >= 3.2}
BuildRequires:  aaa < 3.2.1
BuildRequires:  bbb
BuildRequires:  eee = %{version}-%{release}
BuildRequires:  iii <= 4.2.1
BuildRequires:  jjj > %{version}
BuildRequires:  kkk
BuildRequires:  rrr >= %{version}
BuildRequires:  zzz
Requires:       aaa < 3.2.1
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
# FIXME: use proper Requires(pre/post/preun/...)
PreReq:         aaa
PreReq:         aaa < 3.2.1
PreReq:         eee = %{version}-%{release}
PreReq:         iii <= 4.2.1
PreReq:         jjj > %{version}
PreReq:         kkk
PreReq:         rrr >= %{version}
PreReq:         zzz

%changelog
