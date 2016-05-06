

%define root %{version}
%global test somethingelse
%if 0%{?suse_version} > 1230
%bcond_without systemd
%else
%bcond_with    systemd
%endif
%bcond_with self_hosting
Source:         testfile.tar.bz2
Source2:        testfile2.tar.bz2
Source15:       anothersource.tar.xz
Patch0:         test
# This patch is improperly described but we are okay with it
Patch10:        test2

%prep
%setup -q
%setup -q -a1
%setup -q -b2
%setup -q -n %{name}-%{version}-src
%patch10 -p4
%patch0 -p1

%changelog
