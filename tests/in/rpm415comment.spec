#
# spec file for package specRPM_CREATION_NAME
#
# Copyright (c) specCURRENT_YEAR SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


Name:           test-rpm415-comment
Version:        1.0
Release:        0
Summary:        Test rpm 4.15+ comment
License:        MIT

%dnl this is just a comment
%prep
%autosetup

%build
%configure
%make_build

%install
%make_install

%post
%postun

%files
%license COPYING
%doc ChangeLog README

%changelog
