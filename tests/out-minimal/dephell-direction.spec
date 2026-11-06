%prep
%setup -q
dephell deps convert --from setup.py --to pyproject.toml
dephell deps convert --from pyproject.toml --to setup.py
dephell deps convert
dephell deps convert --from ./pyproject.toml --to setup.py
dephell deps convert --from "pyproject.toml" --to setup.py
dephell deps convert --from "./pyproject.toml" --to ./setup.py
dephell deps convert --from 'pyproject.toml' --to 'setup.py'
dephell deps convert --from ./setup.py --to pyproject.toml

%changelog
