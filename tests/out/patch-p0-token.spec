%prep
%setup -q
%patch -P 0 -p01
%patch -P 12
%patch -P 0 -b foo-p0
%patch -P 0

%changelog
