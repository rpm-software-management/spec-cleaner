#
# spec file for package requires
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
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
# FIXME: use proper Requires(pre/post/preun/...)
PreReq:         aaa < 3.2.1
# FIXME: use proper Requires(pre/post/preun/...)
PreReq:         bbb
PreReq:         eee = %{version}
PreReq:         iii <= 4.2.1
PreReq:         jjj > %{version}
# FIXME: use proper Requires(pre/post/preun/...)
PreReq:         kkk
PreReq:         rrr >= %{version}
PreReq:         zzz

