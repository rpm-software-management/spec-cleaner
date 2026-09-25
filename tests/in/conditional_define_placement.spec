Name:           conditional-define-placement
Version:        1.0
Release:        0
Summary:        test
License:        BSD-3-Clause

# The %if block with %define appears before the top-level defines in the
# input. Placement must be based on the block's content (has defines -> with
# defines), not on whether the parent has seen defines yet. Otherwise the
# block moves between pass 1 and pass 2 (non-idempotent).
%if 0%{?suse_version} <= 1500
%define gccver 13
%endif

%define sonum 2500
%define testing_commit 9ff285c88565f0f6abc855918c6a342e70e4909c

%description
test

%files
