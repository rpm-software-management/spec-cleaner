#
# spec file for package preamble-cond-subpackages
#
# Copyright (c) 2026 SUSE LLC and contributors
#
%define _dracutmodulesdir %(pkg-config --variable dracutmodulesdir dracut)
%if 0%{?suse_version} >= 1540
%bcond_without python
%else
%bcond_with python
%endif
Name:           preamble-cond-subpackages
Version:        7.1
Release:        0
Summary:        Utilities for the filesystem
License:        GPL-2.0-only
Group:          System/Filesystems
URL:            https://example.org/preamble-cond-subpackages
Source0:        https://example.org/preamble-cond-subpackages-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(udev)
Requires:       coreutils
%if %{with python}
%define         python_subpackage_only 1
%python_subpackages
%endif

%description
Utilities for the filesystem.

%changelog
