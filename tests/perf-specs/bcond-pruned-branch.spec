# An emptied nested block does not turn a branch holding only bconds into a define block
%define top 1
Name:           bcond-pruned-branch
Version:        1.0
Release:        0
Summary:        Test
License:        MIT
%bcond_with bar
%if 0%{?suse_version}
%if 0%{?is_opensuse}
%define flavor opensuse
%endif
%else
%if 0%{?fedora}
%endif
%bcond_with foo
%endif

%description
Test.

%files

%changelog
