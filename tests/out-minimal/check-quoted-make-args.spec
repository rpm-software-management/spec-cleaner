%check
make check TEST_OPTS="--jobs %{?_smp_mflags}"
make check OPTS="foo V=1"
make check OPTS='foo VERBOSE=1'
make check %{?_smp_mflags}
make check V=1
make check VERBOSE=1

%changelog
