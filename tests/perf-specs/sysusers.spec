Source1:        system-user-uucp.conf
BuildRequires:  sysuser-tools

%package -n system-user-uucp
Summary:        System user and group uucp
%sysusers_requires

%build
%sysusers_generate_pre %{SOURCE1} uucp

%pre -n system-user-uucp -f uucp.pre

%files -n system-user-uucp
%defattr(-,root,root)
%dir %attr(0750,uucp,uucp) %{_sysconfdir}/uucp
