# Recursive macros make pyrpm.spec.replace_macros raise RuntimeError;
# the https availability check is best-effort and must not crash.
%define aver %{bver}
%define bver %{aver}
Name:           foo
Version:        1.0
Release:        0
Summary:        test
License:        BSD-3-Clause
Source:         http://example.com/foo-%{aver}.tar.gz

%description
test

%files

%changelog
