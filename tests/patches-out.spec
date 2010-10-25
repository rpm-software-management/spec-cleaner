#
# spec file for package
#
# Copyright (c) 2010 SUSE LINUX Products GmbH, Nuernberg, Germany.
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


# PATCH-MISSING-TAG -- See http://en.opensuse.org/Packaging/Patches
Patch2:         a
# PATCH-MISSING-TAG -- See http://en.opensuse.org/Packaging/Patches
Patch3:         b
# PATCH-MISSING-TAG -- See http://en.opensuse.org/Packaging/Patches
Patch0:         c
# PATCH-MISSING-TAG -- See http://en.opensuse.org/Packaging/Patches
Patch1:         d
# PATCH-MISSING-TAG -- See http://en.opensuse.org/Packaging/Patches
Patch0:         e
# PATCH-MISSING-TAG -- See http://en.opensuse.org/Packaging/Patches
Patch99:        f

%prep
%patch3 -p1
%patch2
%patch99 -p1
%patch0 -p1
%patch1
%patch0 -p1
