#
# spec-cleaner tests
#
Name:           util-macros
Version:        1.0
Release:        0
Summary:        Test package
License:        MIT
URL:            https://example.org/util-macros
Source0:        %{name}-%{version}.tar.gz

%description
Test package.

%build
aclocal
ar rcs libfoo.a foo.o
as -o foo.o foo.S
autoconf
autoheader
automake
bzip2 -k foo
cat foo
chgrp root foo
chmod +x foo
chown root foo
cp foo bar
cpio -o -H newc foo
file foo
gpg --verify foo
grep -q foo bar
gzip foo
id -u
install -m 0755 foo %{buildroot}%{_bindir}/foo
ld foo
libtoolize
%make_build all
mkdir -p dir
mv foo bar
nm foo
objcopy foo
objdump foo
patch -p1 foo.patch
perl -pi -e 's/a/b/' foo
python setup.py build
python2 setup.py build
python3 setup.py build
pypy3 -m pip install
ranlib libfoo.a
restorecon -R %{buildroot}
rm -f foo
rsh host true
sed -i s/a/b/ foo
semodule -i foo.pp
ssh host true
strip foo
tar xf foo.tar
unzip -o foo.zip
xz -d foo.xz
%make_build all
rm -f foo

%files

%changelog
