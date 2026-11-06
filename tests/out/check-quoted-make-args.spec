%check
%make_build check TEST_OPTS="--jobs %{?_smp_mflags}"
%make_build check OPTS="foo V=1"
%make_build check OPTS='foo VERBOSE=1'
%make_build check
%make_build check
%make_build check

%changelog
