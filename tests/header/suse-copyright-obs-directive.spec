#
# spec file for package suse-copyright-obs-directive
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


# Run the test suite by default
%bcond_without tests
Name:           suse-copyright-obs-directive
Version:        1.0
Release:        0
Summary:        Keep OBS directives placed right below the header
License:        MIT
BuildRequires:  gcc
#!BuildIgnore:  post-build-checks

%description
The #!BuildIgnore directive below the header survives the header regeneration.

%changelog
