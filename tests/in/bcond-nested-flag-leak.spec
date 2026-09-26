# An inner bcond block does not decide where its enclosing block goes
Name:           bcond-nested-flag-leak
Version:        1.0
Release:        0
Summary:        Test
License:        MIT
%bcond_without  foo
%if 0%{?suse_version}
%if %{with foo}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%endif
%bcond bar %{with foo}
%endif
Provides:       bar-%{?with_bar:on}%{!?with_bar:off}

%description
Test.

%files

%changelog
