Name:           foo
Version:        1.0
Release:        0
Summary:        test
License:        BSD-3-Clause
# The https availability probe must match the Source against pyrpm's
# sources even when macro bracing differs (%dlpath vs %{dlpath}).
%define dlpath status/200
Source:         http://httpbin.org/%dlpath

%description
test

%files
