# A kernel_module global reading the version keeps its define block below the tags
Name:           global-late-kernel-module-block
Version:        1.0
Release:        0
Summary:        Test
License:        MIT
%if 0%{?suse_version}
%define flavor suse
%global kernel_module_ver %{version}
%endif

%description
Test.

%files

%changelog
