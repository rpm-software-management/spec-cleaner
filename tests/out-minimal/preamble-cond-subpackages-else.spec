#
# spec file for package preamble-cond-subpackages-else
#
# Copyright (c) 2026 SUSE LLC and contributors
#
Name:           preamble-cond-subpackages-else
Version:        1.0
Release:        0
Summary:        Utilities for the filesystem
License:        GPL-2.0-only
Group:          System/Filesystems
URL:            https://example.org/preamble-cond-subpackages-else
Source0:        https://example.org/preamble-cond-subpackages-else-%{version}.tar.gz
BuildRequires:  gcc
%if 0%{?suse_version} >= 1550
# TW: generate subpackages for every python3 flavor
%define python_subpackage_only 1
%python_subpackages
%else
%define python_sitelib %{python3_sitelib}
%endif

%description
Utilities for the filesystem.

%changelog
