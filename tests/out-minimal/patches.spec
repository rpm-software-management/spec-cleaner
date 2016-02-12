#
# spec file for package patches
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
%patch -p1
%patch -P 10
%patch -p1  -P 	11
%patch  -P12 	-p0
%patch -P11 -p3
%patch -P20 -P30

%changelog
