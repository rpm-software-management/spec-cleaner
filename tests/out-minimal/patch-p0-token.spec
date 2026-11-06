%prep
%setup -q
%patch -p01
%patch -P 12 -p0
%patch -b foo-p0
%patch -p0

%changelog
