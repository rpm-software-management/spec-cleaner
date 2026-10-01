Name:           test
Version:        1.0
Release:        0
Summary:        test
License:        MIT
Group:          test

%description
test

%define my_install() \
   %%{__unzip} -q -d "$1" \
   %%__unzip -q -d "$1" \
   %%{nil}

%build
%my_install foo.zip

%changelog
