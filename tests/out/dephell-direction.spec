%prep
%setup -q
dephell deps convert --from setup.py --to pyproject.toml
%dephell_gensetup
dephell deps convert
%dephell_gensetup
%dephell_gensetup
%dephell_gensetup
%dephell_gensetup
dephell deps convert --from ./setup.py --to pyproject.toml

%changelog
