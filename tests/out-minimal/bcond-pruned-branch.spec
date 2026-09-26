# An emptied nested block does not turn a branch holding only bconds into a define block
%define top 1
%bcond_with bar
%if 0%{?suse_version}
%if 0%{?is_opensuse}
%define flavor opensuse
%endif
%else
%bcond_with foo
%endif
Name:           bcond-pruned-branch
Version:        1.0
Release:        0
Summary:        Test
License:        MIT

%description
Test.

%files

%changelog
