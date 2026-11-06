%define myvar something-kernel_module
Name:           kernel-module-define-name
Version:        1.0
Release:        0
Summary:        Test
License:        MIT
%define kernel_module_plain 1
%global kernel_module_ver %{version}
%global other_global %{kernel_module_ver}-suffix
%{?suse_kernel_module_package:%{suse_kernel_module_package} -p %{name}-kmp}

%description
Test.

%files

%changelog
