# The value of a %patch option is not a patch number, so only -P renumbers
Name:           patch-option-value
Version:        1.0
Release:        0
Summary:        Do not read a %patch option value as a patch number
License:        MIT
URL:            https://example.com
Patch:          bare.patch

%description
The value of -p, -b, -z, -F, -d and -o is not a patch number, so a
%patch naming only those options still needs the '-P 0' the bare Patch
tag requires.

%prep
%setup -q
%patch -p 1
%patch -b 1
%patch -z 1
%patch -F 1
%patch -d 1
%patch -o 1

%changelog
