%prep
%setup -n %{name}-%{version} -qa 1
%setup -n foo-src -qT
%setup -n foo -qc
%setup -a 1 -qT
%setup -qn %{name}-%{version}
%setup -T -qa1
