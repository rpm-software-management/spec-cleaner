#
# spec file for package providesobsoletes
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


%package -n %{libname}
Summary:        Library for Importing WordPerfect (tm) Documents
Group:          System/Libraries
# remove the old non-versioned package (built in the bs for instance)
Provides:       libwpd = %{version}
Obsoletes:      libwpd < %{version}
Provides:       sysvinit:/sbin/init

%changelog
