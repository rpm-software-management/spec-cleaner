# A kernel_module global reading the version keeps its define block below the tags
Name:           global-late-kernel-module-block
Version:        1.0
Release:        0
%if 0%{?suse_version}
%define flavor suse
%global kernel_module_ver %{version}
%endif
Summary:        Test
License:        MIT

%description
Test.

%files

%changelog
