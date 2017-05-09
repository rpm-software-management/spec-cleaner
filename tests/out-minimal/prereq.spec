Name:           prereq
PreReq:         %fillup_prereq
PreReq:         %insserv_prereq
PreReq:         %{_bindir}/chroot
PreReq:         /bin/mkdir
PreReq:         /bin/rm
PreReq:         deprecatedrequires
PreReq:         uglyline1
PreReq:         uglyline2
Requires(post): asomething
Requires(post): bsomething
Requires(post): something
Requires(postun): somethingcrazy
Requires(pre):  test1

%changelog
