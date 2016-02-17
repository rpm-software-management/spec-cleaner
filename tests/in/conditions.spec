Version:        2.8.2
Release:        0
Summary:        AppArmor userlevel parser utility
License:        GPL-2.0+
Group:          Productivity/Networking/Security
Source0:        apparmor-%{version}.tar.gz
Source1:        apparmor-%{version}.tar.gz.asc
Source2:        %{name}.keyring
%if %{distro} == "suse"
PreReq:         %{insserv_prereq}
PreReq:         aaa_base
%endif
BuildRequires:  pkg-config
BuildRequires:  python
%{if %{with editor}}
%ifarch ppc64
Requires:       naughty-stuff
%endif # test commentary
BuildRequires:  gcc-c++
BuildRequires:  update-desktop-files
%endif
BuildRequires:  bbb
Requires:       insserv
%if (0%{?suse_version} && 0%{?suse_version} >= 1210)
Requires: wine
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-build
