%build
pushd bulshit
# FIXME: you should use the %%configure macro
	./configure
  make %{?_smp_mflags}
popd

%changelog
