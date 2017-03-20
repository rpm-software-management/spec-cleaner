#
# spec file for package sysusers
#
# Copyright (c) 2017 SUSE LINUX GmbH, Nuernberg, Germany.
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


Source1:        system-user-uucp.conf
BuildRequires:  sysuser-tools

%package -n system-user-uucp
Summary:        System user and group uucp
%sysusers_requires

%build
%sysusers_generate_pre %{SOURCE1} uucp

%pre -n system-user-uucp -f uucp.pre

%files -n system-user-uucp
%defattr(-,root,root)
%dir %attr(0750,uucp,uucp) %{_sysconfdir}/uucp

%changelog
