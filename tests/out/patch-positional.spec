%prep
%setup -q
%patch 0 -p1
%patch 1 -p1
%patch 2 3
%patch -p1 4
%patch -p1 -b .orig 5
%patch %{patchnum} -p1
%patch -P 0 -F 3 -p1
%patch -P 0 -p1

%changelog
