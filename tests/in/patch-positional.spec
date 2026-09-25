%prep
%setup -q
%patch 0 -p1
%patch 1 -p1
%patch 2 3
%patch -p1 4
%patch -p1 -b .orig 5
%patch %{patchnum} -p1
%patch -F 3 -p1
%patch -p1
