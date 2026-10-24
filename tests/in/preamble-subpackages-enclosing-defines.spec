#
# spec file for package preamble-subpackages-enclosing-defines
#
# Copyright (c) 2026 SUSE LLC and contributors
#
Name:           preamble-subpackages-enclosing-defines
Version:        1.0
Release:        0
Summary:        Utilities for the filesystem
License:        GPL-2.0-only
Group:          System/Filesystems
URL:            https://example.org/preamble-subpackages-enclosing-defines
Source0:        https://example.org/preamble-subpackages-enclosing-defines-%{version}.tar.gz
%if 0%{?suse_version} >= 1550
BuildRequires:  %{python_module devel}
%python_subpackages
%else
%define have_python3 0
%endif

%description
Utilities for the filesystem.

%changelog
