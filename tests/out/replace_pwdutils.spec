Name:           at
Version:        3.1.23
Release:        0
Summary:        A Job Manager
License:        GPL-2.0-or-later
Group:          System/Daemons
URL:            https://ftp.debian.org/debian/pool/main/a/at
Source:         https://ftp.debian.org/debian/pool/main/a/at/%{name}_%{version}.orig.tar.gz
BuildRequires:  autoconf >= 2.69
BuildRequires:  automake
BuildRequires:  pam-devel
BuildRequires:  pwdutils
Requires:       libmariadb
Requires:       pwdutils-util
Requires:       shadow
Requires(post): shadow
Requires(post): update-alternatives
Requires(posttrans): shadow
Requires(posttrans): systemd
Requires(postun): shadow
Requires(postun): update-alternatives
Requires(pre):  apache2
Requires(pre):  shadow
Requires(pretrans): shadow
Requires(pretrans): update-alternatives
Requires(preun): chkconfig
Requires(preun): shadow
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

%changelog
