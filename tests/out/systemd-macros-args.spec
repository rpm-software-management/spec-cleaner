%pre
%systemd_pre foo.service
%systemd_user_pre foo.service
%sysusers_create_package foo %{SOURCE1}

%post
%systemd_post foo.service
%systemd_user_post foo.service
%sysctl_apply 50-foo.conf
%binfmt_apply foo.conf

%preun
%systemd_preun foo.service
%systemd_user_preun foo.service

%postun
%systemd_postun bar.service
%systemd_postun_with_restart foo.service
%systemd_user_postun bar.service
%systemd_user_postun_with_restart foo.service

%files

%changelog
