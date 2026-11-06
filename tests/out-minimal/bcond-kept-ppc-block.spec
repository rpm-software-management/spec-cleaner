# A ppc64 block holding a bcond is kept and placed without error
Name:           bcond-kept-ppc-block
Version:        1.0
Release:        0
Summary:        Test
License:        MIT
# bug437293
%ifarch ppc64
%bcond_with 64bit
%endif

%description
Test.

%files

%changelog
