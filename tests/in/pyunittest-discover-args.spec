%check
%python_exec -m unittest discover -v
%python_exec -m unittest discover -s tests -t .
%python_exec -m unittest discover -p "test_*.py"
%python_exec -m unittest discover tests
%python_expand PYTHONPATH=%{buildroot}%{$python_sitelib} $python -m unittest discover -v -s test
%python_expand PYTHONPATH=%{buildroot}%{$python_sitearch} $python -m unittest discover -s test -v
%python_expand PYTHONPATH=%{buildroot}%{$python_sitearch} $python -m unittest discover
