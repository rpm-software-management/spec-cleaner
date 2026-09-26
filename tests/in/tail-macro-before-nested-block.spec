# A tail macro kept in a block does not move with the nested block after it
Name:           tail-macro-before-nested-block
Version:        1.0
Release:        0
Summary:        Test
License:        MIT
%if 0%{?suse_version}
%python_subpackages
%bcond_without test
%if %{with test}
%define foo 1
%endif
%endif
%if 0%{?sle_version}
%python_subpackages
%if 0%{?is_opensuse}
%global srcver v%{version}
%endif
%endif

%description
Test.

%files

%changelog
