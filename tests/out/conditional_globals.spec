# Globals inside conditionals must stay with their %if/%endif wrappers;
# moving them out would make them unconditional and corrupt the spec.
%ifnarch x86_64
%global _with_zero 1
%endif
%if 0%{?suse_version} > 1500
%global bits 64
%endif
Name:           foo
Version:        1.0
Release:        0
# A top-level order-sensitive global triggers the late-global split.
%global topver %{version}
Summary:        test
License:        BSD-3-Clause

%description
test

%files

%changelog
