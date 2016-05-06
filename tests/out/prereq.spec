# FIXME: use proper Requires(pre/post/preun/...)
PreReq:         deprecatedrequires
PreReq:         uglyline1
PreReq:         uglyline2
Requires(post): asomething
Requires(post): bsomething
Requires(post): something
Requires(postun): somethingcrazy
Requires(pre):  test1

%changelog
