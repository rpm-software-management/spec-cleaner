%if 0%{?suse_version} > 1500
%define flavor ng
%global tarname tag-macro-ng-%{version}
%else
%define flavor classic
%global tarname tag-macro-%{version}
%endif
%define pkgname global-late-tag-macro-%{flavor}
Name:           %{pkgname}
Version:        1.0
Release:        0
Summary:        Test a block defining a macro the tags use stays above them
License:        MIT
URL:            https://example.org
Source:         %{tarname}.tar.gz

%description
Test.

%changelog
