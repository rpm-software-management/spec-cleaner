#!BuildIgnore: post-build-checks

#!BuildIgnore: post-source-checks
#
# spec file for package suse-copyright-shebang-first
#
# Copyright (c) 2020 SUSE LLC
#
# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

# Run the test suite by default
%bcond_without tests
Name:           suse-copyright-shebang-first
Version:        1.0
Release:        0
Summary:        A leading directive keeps the copyright section open
License:        MIT
BuildRequires:  gcc

%description
Nothing but directives above the blank line, so the second one is
still inside the copyright section and stays in the header.

%changelog
