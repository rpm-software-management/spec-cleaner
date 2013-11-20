Patch2: a
Patch3: b
Patch: c
Patch1: d
Patch0: e
Patch99: f
Patch10: g
Patch11: h
# PATCH-FIX-OPENSUSE fix-for-opensuse-specific-things.patch bnc#123456
Patch12: i

%prep
%patch3 -p1
%patch2
%patch99 -p1
%patch0 -p1
%patch1
%patch -p1
%patch -P 10
%patch -p1  -P 	11
%patch  -P12 	-p0
%patch -P11 -p3
%patch -P20 -P30
