Name:           foo
Version:        1.0
Release:        0
Summary:        Foo
License:        MIT
URL:            https://example.org/

%global mydir %{?name}-data
%global mydir2 %{name}-data
%global mydir3 %{!name:foo}-data
%global mydir4 %{name:foo}-data

%description
Foo.

%files
%{_bindir}/foo

%changelog
