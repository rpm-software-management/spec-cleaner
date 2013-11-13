source: testfile.tar.bz2
Patch10: test2
Source2: testfile2.tar.bz2
Patch: test

%setup
%patch10 -p4
%patch -p1
