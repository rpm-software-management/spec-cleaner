%prep
%autosetup -p1 -n %{modname}-v.%{version}
dephell deps convert --traceback --level=DEBUG --from pyproject.toml --to setup.py

%changelog
