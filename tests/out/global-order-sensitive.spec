Name:           foo
Version:        1.0
Release:        0
%global mydir %{?name}-data
%global mydir2 %{name}-data
%global mydir3 %{!name:foo}-data
%global mydir4 %{name:foo}-data
Summary:        Foo
License:        MIT
URL:            https://example.org/

%description
Foo.

%files
%{_bindir}/foo

%changelog
