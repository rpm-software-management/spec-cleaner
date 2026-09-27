# 2022 William Brown
#
# spec file for package suse-copyright-year-first
#
# Copyright (c) 2020 SUSE LLC
#
# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

# Run the test suite by default
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
