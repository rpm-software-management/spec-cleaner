#
# spec file for package generated
#
# Copyright (c) 2013 SUSE LLC and contributors
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
##### WARNING: Please do not edit this auto generated spec file.
#

Name:           generated
Version:        1.0
Release:        0
Summary:        Generated package
License:        MIT
Group:          System/Base
Url:            http://example.org/
Source:         generated-1.0.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Generated package. The formatting of this file is exactly what the
generator wrote and it stays that way.

%prep
%setup -q

%build
make %{?_smp_mflags} CFLAGS="%{optflags}"

%install
make install DESTDIR=%{buildroot} %{?_smp_mflags}

%files
%defattr(-,root,root)
%doc README

%changelog
