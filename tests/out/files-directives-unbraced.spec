Name:           files-directives-unbraced
Version:        1.0
Release:        0
Summary:        Test that rpm file directives are not curlified
License:        MIT
URL:            https://example.org/

%description
Test.

%files
%defverify(not md5 size mtime)
%attr(0666,root,root) %dev(c,1,3) /dev/null
%dev(c, 5, 1) /dev/console
%missingok %{_sysconfdir}/%{name}.d
%pubkey %{_datadir}/%{name}/key.asc
%artifact %{_libdir}/%{name}.debug
%readme README

%changelog
