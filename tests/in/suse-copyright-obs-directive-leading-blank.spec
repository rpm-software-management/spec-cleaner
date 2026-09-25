
#!BuildIgnore: post-build-checks
#
# spec file for package suse-copyright-obs-directive-leading-blank
#
# Copyright (c) 2020 SUSE LLC
# Copyright (c) 2019 Jane Doe
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


Name:           suse-copyright-obs-directive-leading-blank
Version:        1.0
Release:        0
Summary:        Keep OBS directives placed above the header after a blank line
License:        MIT

%description
A blank first line before the #!BuildIgnore directive does not duplicate the header.

%changelog
