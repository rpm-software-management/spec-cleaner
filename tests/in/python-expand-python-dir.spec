%build
%python_expand make -C python install DESTDIR=%{buildroot} PYTHON=$python
%python_expand cp -r python %{buildroot}%{python_sitelib}/
%{python_expand cd python && python setup.py build}
%python_expand xvfb-run -a python -m pytest
%python_expand PYTHONPATH=%{buildroot}%{python_sitelib} python tests/run
