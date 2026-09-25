# This is NOT a bcond test (%{bar} is a plain macro, not %{with bar}).
# The _condition_bcond flag must not leak from the previous block;
# this block has defines and must go with defines, not bcond_conditions.
%if %{bar}
%define bar_enabled 1
%endif
%define top_level 1
%bcond_with foo
%bcond_without bar
# This is a bcond test: goes to bcond_conditions.
%if %{with foo}
%define with_foo 1
%endif
Name:           conditional-bcond-sticky
Version:        1.0
Release:        0
Summary:        test
License:        BSD-3-Clause

%description
test

%files

%changelog
