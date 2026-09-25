%files
%doc %attr(0644,root,root) LICENSE
%doc %attr(0644, root, root) COPYING README
%doc %lang(de) LIESMICH COPYING.de
%doc %verify(not md5 size mtime) LICENSE.txt NEWS
%doc %config(noreplace) %{_sysconfdir}/foo.conf LICENSE
%doc README COPYING
%{_bindir}/foo
