%check
%python_expand PYTHONPATH=%{buildroot}%{$python_sitelib} py.test-%{$python_version}
%python_expand py.test-%{$python_version}
%python_expand PYTHONPATH=%{buildroot}%{$python_sitelib} $python py.test-%{$python_version}
%python_expand PYTHONPATH=%{buildroot}%{$python_sitelib} $python %{_bindir}/py.test -o addopts=-v
%python_expand PYTHONPATH=%{buildroot}%{$python_sitelib} py.test-%{$python_bin_suffix}
%python_expand PYTHONPATH=%{buildroot}%{$python_sitelib} %{_bindir}py.test-%{$python_bin_suffix} -v
%python_expand PYTHONPATH=%{buildroot}%{$python_sitelib} pytest
%python_expand PYTHONPATH=%{buildroot}%{$python_sitelib} $python -m pytest
%python_exec %{_bindir}/py.test -v
%python_expand PYTHONPATH=%{buildroot}%{$python_sitearch} py.test-%{$python_bin_suffix}
%python_exec -m pytest -v
%python_exec -m pytest -o addopts=-v
%python_expand PYTHONPATH=%{buildroot}%{$python_sitelib} py.test-%{$python_bin_suffix} -v src/txacme/test -k 'not (matchers or util or client)'

%changelog
