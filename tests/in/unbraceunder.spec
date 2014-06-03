%post
%insserv_cleanup
%service_add_pre
current=$(cd "%_libdir/icu/"; find [0-9]* -maxdepth 1 -type d -printf '%f\n' |
