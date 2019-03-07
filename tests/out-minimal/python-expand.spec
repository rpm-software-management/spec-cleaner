%install
%python_expand %fdupes %{buildroot}%{$python_sitelib}
%python_expand %fdupes %{buildroot}%{$python_sitearch}


%check
%python_expand PYTHONPATH=%{$python_sitearch} nosetests-%{$python_bin_suffix}
%python_expand testr-%{$python_version}
%{python_expand $python -m unittest discover}

%changelog
