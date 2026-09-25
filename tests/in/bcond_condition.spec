Name:           bcond_condition
Version:        1.0
Release:        0
Summary:        Test conditional bcond placement
License:        BSD-3-Clause
Group:          Development/Tools/Other
%define         somevar 1
%bcond_with     extra
%if 0%{?suse_version} <= 1550
# enable precompiled profile cache on <= 15.x
%bcond_without precompiled_cache
%else
# keep it off elsewhere
%bcond_with precompiled_cache
%endif

%description
Test conditional bcond placement.

%files

%changelog
