Name:           remove-groups-comments
Version:        1.0
Release:        0
Summary:        Test
License:        MIT
# FIXME: use correct group or remove it, see "https://en.opensuse.org/openSUSE:Package_group_guidelines"
Group:          Whatever
URL:            https://example.com

%description
Test.

%package devel
Summary:        Devel files
# devel files belong here
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}

%description devel
Devel files.

%changelog
