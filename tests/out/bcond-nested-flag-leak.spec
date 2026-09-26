# An inner bcond block does not decide where its enclosing block goes
%bcond_without  foo
%if 0%{?suse_version}
%bcond bar %{with foo}
%endif
Name:           bcond-nested-flag-leak
Version:        1.0
Release:        0
Summary:        Test
License:        MIT
Provides:       bar-%{?with_bar:on}%{!?with_bar:off}

%description
Test.

%files

%changelog
