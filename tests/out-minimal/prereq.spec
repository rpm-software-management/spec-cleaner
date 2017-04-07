PreReq:         /bin/rm
PreReq:         /bin/mkdir
PreReq:         /usr/bin/chroot
PreReq:         %fillup_prereq
PreReq:         %insserv_prereq
PreReq:         deprecatedrequires
PreReq:         uglyline1
PreReq:         uglyline2
Requires(post): asomething
Requires(post): bsomething
Requires(post): something
Requires(postun): somethingcrazy
Requires(pre):  test1

%changelog
