#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# PATCH-MISSING-TAG -- See http://en.opensuse.org/openSUSE:Packaging_Patches_guidelines
Patch2:         a
# PATCH-MISSING-TAG -- See http://en.opensuse.org/openSUSE:Packaging_Patches_guidelines
Patch3:         b
# PATCH-MISSING-TAG -- See http://en.opensuse.org/openSUSE:Packaging_Patches_guidelines
Patch0:         c
# PATCH-MISSING-TAG -- See http://en.opensuse.org/openSUSE:Packaging_Patches_guidelines
Patch1:         d
# PATCH-MISSING-TAG -- See http://en.opensuse.org/openSUSE:Packaging_Patches_guidelines
Patch0:         e
# PATCH-MISSING-TAG -- See http://en.opensuse.org/openSUSE:Packaging_Patches_guidelines
Patch99:        f

%prep
%patch3 -p1
%patch2
%patch99 -p1
%patch0 -p1
%patch1
%patch0 -p1
