#
# spec-cleaner tests
#
Name:           util-macros-compound
Version:        1.0
Release:        0
Summary:        Test package
License:        MIT
URL:            https://example.org/util-macros-compound
Source0:        %{name}-%{version}.tar.gz

%description
Test package.

%build
%__id_u
%__ln_s foo bar
xz --format=lzma -d foo.xz
%__mkdir_p dir
gawk '{print $1}' foo
gcc foo.c
gcc -E foo.c
g++ foo.cc
rsh host true
%__id_u
%__mkdir_p dir

%files

%changelog
