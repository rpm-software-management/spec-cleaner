#
# spec file for package conditiondefreq
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


%if xxx
%define something xxx
%else
%define something yyy
%endif
%if %something
%define something2 xxx
%else
%define something2 yyy
%endif
%if %something2
%define crazystuff value
BuildRequires:  variable
%endif
Name:           something
Version:        something
BuildRequires:  something
%if %something2
Requires:       ddd
%endif

%changelog
