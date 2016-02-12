#
# spec file for package filesattr
#
# Copyright (c) 2013 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


%files
%doc %lang(en) %{_prefix}/bla
%dir %attr(0710,root,lp) %{_var}/spool/cups
%dir %attr(1770,root,lp) %{_var}/spool/cups/tmp
%dir %attr(0755,lp,lp) %{_var}/log/cups/
%dir %attr(0775,lp,lp) %{_var}/cache/cups
%attr(555,root,root) %{_libdir}/security/pam_apparmor.so
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%{1}/modules/active/policy.kern
%config(noreplace) /a/b/c

%changelog
