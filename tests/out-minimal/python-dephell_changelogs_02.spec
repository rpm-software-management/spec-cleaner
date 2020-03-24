%prep
%autosetup -p1 -n %{modname}-v.%{version}
dephells convert --traceback --level=DEBUG --from pyproject.toml --to setup.py

%changelog
