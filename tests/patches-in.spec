Patch2: a
Patch3: b
Patch: c
Patch1: d
Patch0: e
Patch99: f

%prep
%patch3 -p1
%patch2
%patch99 -p1
%patch0 -p1
%patch1
%patch -p1
