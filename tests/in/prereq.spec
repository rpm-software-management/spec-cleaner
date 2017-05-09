Name:           prereq
Requires(post): something
Requires(pre): test1
Requires(post): asomething bsomething
PreReq: deprecatedrequires
PreReq: uglyline1 uglyline2
PreReq: /bin/rm /bin/mkdir /usr/bin/chroot %fillup_prereq %insserv_prereq
Requires(postun): somethingcrazy
