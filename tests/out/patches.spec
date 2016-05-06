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
%patch3 -p1
%patch2
%patch99 -p1
%patch0 -p1
%patch1
%patch0 -p1
%patch10
%patch11 -p1
%patch12
%patch11 -p3
%patch -P20 -P30

%changelog
