#
# spec file for package sourcespatches
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


# this is crazy define
%define root %{version}
%global test somethingelse
%if 0%{?suse_version} > 1230
%bcond_without systemd
%else
%bcond_with    systemd
%endif
%bcond_with self_hosting
Source:         testfile.tar.bz2
Source2:        testfile2.tar.bz2
Source15:       anothersource.tar.xz
Patch0:         test
# This patch is improperly described but we are okay with it
Patch10:        test2

%prep
%setup -q
%setup -q -a1
%setup -q -b2
%setup -q -n %{name}-%{version}-src
%patch10 -p4
%patch0 -p1

%changelog
