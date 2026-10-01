Name:           test
Version:        1.0
Release:        0
Summary:        test
License:        MIT
# FIXME: use correct group or remove it, see "https://en.opensuse.org/openSUSE:Package_group_guidelines"
Group:          test

%description
test

%define my_install() \
   %%{__unzip} -q -d "$1" \
   %%{nil}

%build
%my_install foo.zip

%changelog
