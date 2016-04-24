#
# spec file for package ppcoldsupport
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


%package libcap
Requires:       bash
# bug437293
%ifarch ppc64
Obsoletes:      libcap-64bit
%endif

%package libcap-devel
BuildRequires:  pkgconfig
# bug437293
%ifarch ppc64
Obsoletes:      libcap-devel-64bit
%endif

%package crazypackage
Requires:       weirddep
# bug437293
%ifarch ppc64
Obsoletes:      libcap-devel-32bit
%endif

%package crazypackage2
Requires:       weirddep
# bug437293
%ifarch ppc64
BuildRequires:  somethinghandwritten
Obsoletes:      libcap-devel-64bit
%endif

%changelog
