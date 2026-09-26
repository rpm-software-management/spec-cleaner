# A pruned ppc64 block holding a bcond is placed without error
# bug437293
%ifarch ppc64
%bcond_with 64bit
%endif
Name:           bcond-pruned-ppc-block
Version:        1.0
Release:        0
Summary:        Test
License:        MIT

%description
Test.

%files

%changelog
