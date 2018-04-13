%{?!_fillupdir:%define _fillupdir %{_localstatedir}/adm/fillup-templates}
%if 0%{?suse_version} == 1110
# _libexecdir points to /usr/lib64 for SLE11
%define _libexecdir /lib
%endif
Version:        2.8.2
Summary:        AppArmor userlevel parser utility
License:        GPL-2.0-or-later
Group:          Productivity/Networking/Security
Source0:        apparmor-%{version}.tar.gz
Source1:        apparmor-%{version}.tar.gz.asc
Source2:        %{name}.keyring
BuildRequires:  bbb
BuildRequires:  pkgconfig
BuildRequires:  python
Requires:       insserv
%ifpython2
Release:        0
%endif
%if %{distro} == "suse"
PreReq:         %{insserv_prereq}
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
%if %{?pkg_vcmp:%pkg_vcmp java-devel >= 9}%{!?pkg_vcmp:0}
Requires:       other
%endif
%if (0%{?sle_version} == 120100 && 0%{?is_opensuse} == 0) || 0%{?suse_version} == 1310
Requires:       something
%endif

%changelog
