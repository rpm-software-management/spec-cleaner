%package libcap
Requires:       bash

%package libcap-devel
BuildRequires:  pkgconfig

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
