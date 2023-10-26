Name:           at
Version:        3.1.23
Release:        0
Summary:        A Job Manager
License:        GPL-2.0-or-later
Group:          System/Daemons
URL:            https://ftp.debian.org/debian/pool/main/a/at
Source:         http://ftp.debian.org/debian/pool/main/a/at/%{name}_%{version}.orig.tar.gz
BuildRequires:  autoconf >= 2.69
BuildRequires:  automake
BuildRequires:  pam-devel
BuildRequires:  pwdutils
Requires(post): pwdutils
Requires(post): update-alternatives
Requires(posttrans): pwdutils
Requires(posttrans): systemd
Requires(postun): pwdutils
Requires(postun): update-alternatives
Requires(pre):  pwdutils
Requires(pre):  apache2
Requires(pretrans): pwdutils
Requires(pretrans): update-alternatives
Requires(preun): pwdutils
Requires(preun): chkconfig
Requires:       pwdutils
Requires:       libmariadb
Requires:       pwdutils-util
Recommends:     smtp_daemon

%ifarch x86_64
Requires(pre):  pwdutils
%else
Requires(pre):  shadow
%endif

%if 0%{old_RHEL} > 0
Requires(post): pwdutils
Requires(pre):  pwdutils
%endif

%if 0%{with_tokudb} > 0
Requires:       pwdutils
%endif

%if 0%{?suse_version} >= 1320 || 0%{?is_opensuse}
Requires(pre):  pwdutils
%else
Requires(pre):  shadow
%endif

%if 0%{?suse_version} <= 1140
Requires(post): shadow
%else
Requires(post): pwdutils
%endif
