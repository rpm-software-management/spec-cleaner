%check
%python_expand PYTHONPATH=%{buildroot}%{$python_sitelib} $python -m unittest discover
%python_expand PYTHONPATH=%{buildroot}%{$python_sitelib} $python -m unittest discover -v
%python_exec -m unittest discover tests -v
%python_exec -m unittest discover
%python_exec -m unittest discover -v -s tests
%python_exec -m unittest -v tests.test_cursors
%python_expand PYTHONPATH=%{buildroot}%{$python_sitelib} $python -m unittest openid.test.test_suite
%python_expand PYTHONPATH=%{buildroot}%{$python_sitearch} $python -m unittest discover -v
