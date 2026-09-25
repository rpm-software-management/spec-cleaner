Name:           foo
Version:        1.0
Release:        0
Summary:        test
License:        BSD-3-Clause
# A top-level order-sensitive global triggers the late-global split.
%global topver %version

# Globals inside conditionals must stay with their %if/%endif wrappers;
# moving them out would make them unconditional and corrupt the spec.
%ifnarch x86_64
%global _with_zero 1
%endif
%if 0%{?suse_version} > 1500
%global bits 64
%endif

%description
test

%files
