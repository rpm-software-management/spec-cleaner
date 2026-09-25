%check
%python_expand $python -m pytest -vv tests
%python_expand $python -m pytest -vs tests
%python_exec -m pytest -vvv
%python_expand PYTHONPATH=%{buildroot}%{$python_sitearch} py.test-%{$python_bin_suffix} -vx tests
%python_expand pytest-%{$python_bin_suffix} -vrs tests
%python_expand $python -m pytest -o addopts=-vv tests
%python_expand $python -m pytest -v tests
