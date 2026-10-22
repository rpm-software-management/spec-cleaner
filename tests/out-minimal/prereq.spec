Name:           prereq
Requires(post): something
Requires(pre):  test1
Requires(post): asomething
Requires(post): bsomething
PreReq:         deprecatedrequires
PreReq:         uglyline1
PreReq:         uglyline2
PreReq:         /bin/rm
PreReq:         /bin/mkdir
PreReq:         %{_bindir}/chroot
PreReq:         %fillup_prereq
PreReq:         %insserv_prereq
Requires(postun): somethingcrazy

%changelog
