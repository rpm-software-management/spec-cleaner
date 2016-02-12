#
# spec file for package rpmcallpkg
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


%if %{with kde4}
%package -n %{name}-client-kde4
Summary:        KDE 4 Backend for sflphone
Group:          Productivity/Telephony/SIP/Clients
Requires:       %{name} = %{version}-%{release}
# For building with KDE 4.12
# % kde4_akonadi_requires == "Requires: akonadi-runtime  >= 1.10.2 akonadi-runtime < 1.10.40" (on openSUSE 13.1)
Requires:       akonadi-runtime >= %( echo `rpm -q --queryformat '%{VERSION}' akonadi-runtime`)
%kde4_runtime_requires
%kde4_pimlibs_requires

%description -n %{name}-client-kde4
KDE 4 backend for SFLphone.
%endif

%changelog
