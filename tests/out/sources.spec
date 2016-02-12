#
# spec file for package sources
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


Source1:        something
Source2:        somethingelse
Source200:      ou
Source300:      godknowswhat
NoSource:       2
NoSource:       300
%setup -q
cp %{SOURCE1} %{buildroot}
cp %{SOURCE2} %{buildroot}
cp %{SOURCE200} %{buildroot}
cp %{SOURCE300} %{buildroot}

%changelog
