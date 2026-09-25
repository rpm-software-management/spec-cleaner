%prep
%setup -q -a 1
%setup -q -n foo-src -T
%setup -q -n foo -c
%setup -q -a 1 -T
%setup -q
%setup -q -T -a1

%changelog
