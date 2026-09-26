%if 0%{?suse_version}
# Nested bcond block: marks its parent as containing defines.
%if 1
%bcond_with foo
%endif
# The define flag must not leak from the bcond block above into this
# sibling block. It only has BuildRequires and must stay with the build
# conditions at the bottom, keeping the input order stable.
%if 0%{?sle_version}
BuildRequires:  bar
%endif
%endif
Name:           conditional-define-flag-leak
Version:        1.0
Release:        0
Summary:        test
License:        BSD-3-Clause

%description
test

%files

%changelog
