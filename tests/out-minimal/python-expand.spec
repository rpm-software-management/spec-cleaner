%install
%python_expand %fdupes %{buildroot}%{$python_sitelib}
%python_expand %fdupes %{buildroot}%{$python_sitearch}
%python_expand rm %{buildroot}%{_bindir}/foo-%{python_version_nodots}


%check
%python_expand PYTHONPATH=%{$python_sitearch} nosetests-%{$python_bin_suffix}
%python_expand testr-%{$python_version}
%{python_expand $python -m unittest discover}

%changelog
