%pre
%selinux_relabel_pre -s targeted

%post
%selinux_modules_install -s targeted /usr/share/selinux/packages/foo.pp.bz2
%selinux_set_booleans -s targeted foo_enabled=on

%postun
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s targeted foo
    %selinux_unset_booleans -s targeted foo_enabled=on
fi

%posttrans
%selinux_relabel_post -s targeted

%files
