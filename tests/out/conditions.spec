Version:        2.8.2
Release:        0
Summary:        AppArmor userlevel parser utility
License:        GPL-2.0+
Group:          Productivity/Networking/Security
Source0:        apparmor-%{version}.tar.gz
Source1:        apparmor-%{version}.tar.gz.asc
Source2:        %{name}.keyring
BuildRequires:  bbb
BuildRequires:  pkgconfig
BuildRequires:  python
Requires:       insserv
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%if %{distro} == "suse"
# FIXME: use proper Requires(pre/post/preun/...)
PreReq:         %insserv_prereq
PreReq:         aaa_base
%endif
%{if %{with editor}}
BuildRequires:  gcc-c++
BuildRequires:  update-desktop-files
%ifarch ppc64
Requires:       naughty-stuff
%endif # test commentary
%endif
%if (0%{?suse_version} && 0%{?suse_version} >= 1210)
Requires:       wine
%endif
%if (0%{?sle_version} == 120100 && 0%{?is_opensuse} == 0) || 0%{?suse_version} == 1310
Requires:       something
%endif

%changelog
