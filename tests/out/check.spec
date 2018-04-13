%check
%make_build V=1 check RUNTEST=true
make -j1 check
%make_build test V=1

%changelog
