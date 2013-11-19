

source: testfile.tar.bz2
Patch10: test2
Source2: testfile2.tar.bz2
Patch: test


%prep
%setup -qn %name-%version
%setup -q -n "%name-%version" -a1
%setup -n "%name-%version" -q -b2
%patch10 -p4
%patch -p1
