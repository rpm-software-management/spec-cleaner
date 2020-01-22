%build
pushd bulshit
# FIXME: you should use the %%configure macro
	./configure
  %make_build
popd

%changelog
