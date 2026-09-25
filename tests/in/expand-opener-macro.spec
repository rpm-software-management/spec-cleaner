Name:           expand-opener
Version:        1.0
Release:        0
%define _description %{expand:The %{?vendor_name} library provides things.
It is great and fast.}
%global pkg_description %{expand:%{name} is a library.
Library for %{name}
It is small.}
Summary:        Test a %%{expand: opener referencing a macro
License:        MIT
URL:            https://example.org/

%description
%{_description}

%changelog
