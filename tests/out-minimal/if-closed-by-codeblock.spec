# a %{?cond: block closed by a codeblock end instead of %endif
Name:           if-closed-by-codeblock
Version:        1.0
Release:        0
Summary:        Test package
License:        MIT
URL:            https://example.org/if-closed-by-codeblock
%if 0%{?suse_version} > 1500
# /SECTION

%description
Test package.

%changelog
