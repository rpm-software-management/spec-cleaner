%if 0%{?suse_version} > 1500
%global lua_version 5.4
%else
%global lua_version 5.3
%endif
%global lua_version_nodots %(echo %{lua_version} | tr -d .)
%define srcname conditional-define-order
Name:           conditional-define-order
Version:        1.0
Release:        0
Summary:        Test a conditional define block keeps its place before later globals
License:        MIT
URL:            https://example.org/

%description
Test.

%files
%{_libdir}/lua%{lua_version_nodots}

%changelog
