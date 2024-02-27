Patch0:         c
Patch0:         e
Patch1:         d
Patch2:         a
Patch3:         b
Patch10:        g
Patch11:        h
# PATCH-FIX-OPENSUSE fix-for-opensuse-specific-things.patch bnc#123456
Patch12:        i
Patch99:        f

%prep
%patch -P 3 -p1
%patch -P 2
%patch -P 99 -p1
%patch -P 0 -p1
%patch -P 1
%patch -P 0 -p1
%patch -P 10
%patch -p1  -P 	11
%patch  -P12
%patch -P11 -p3
%patch -P20 -P30

%changelog
