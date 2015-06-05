%files
%doc %lang(en) /usr/bla
%dir %attr(0710,root,lp) %{_var}/spool/cups
%dir %attr(1770,root,lp) %{_var}/spool/cups/tmp
%dir %attr(0755,lp,lp) %{_var}/log/cups/
%dir %attr(0775,lp,lp) %{_var}/cache/cups
%attr(555,root,root) %{_libdir}/security/pam_apparmor.so
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%{1}/modules/active/policy.kern
%config(noreplace) /a/b/c
