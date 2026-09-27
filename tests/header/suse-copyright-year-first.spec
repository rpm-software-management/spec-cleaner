#
# spec file for package suse-copyright-year-first
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

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%bcond_without tests
Name:           suse-copyright-year-first
Version:        1.0
Release:        0
Summary:        A year led notice as the very first line
License:        MIT
BuildRequires:  gcc

%description
The year led line at the top is a copyright continuation, so it must be
dropped rather than counted as the first line of the notice.

%changelog
