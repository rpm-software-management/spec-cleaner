# The value of a %patch option is not a patch number, so only -P renumbers
Name:           patch-option-value
Version:        1.0
Release:        0
Summary:        Do not read a %patch option value as a patch number
License:        MIT
URL:            https://example.com
Patch0:         bare.patch

%description
The value of -p, -b, -z, -F, -d and -o is not a patch number, so a
%patch naming only those options still needs the '-P 0' the bare Patch
tag requires.

%prep
%setup -q
%patch -P 0 -p 1
%patch -P 0 -b 1
%patch -P 0 -z 1
%patch -P 0 -F 1
%patch -P 0 -d 1
%patch -P 0 -o 1

%changelog
