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
