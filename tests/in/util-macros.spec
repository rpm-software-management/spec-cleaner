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
%{__ar} rcs libfoo.a foo.o
%{__as} -o foo.o foo.S
autoconf
autoheader
automake
%{__bzip2} -k foo
%{__cat} foo
%{__chgrp} root foo
%{__chmod} +x foo
%{__chown} root foo
%{__cp} foo bar
%{__cpio} -o -H newc foo
%{__file} foo
%{__gpg} --verify foo
%{__grep} -q foo bar
%{__gzip} foo
%{__id} -u
%{__install} -m 0755 foo %{buildroot}%{_bindir}/foo
%{__ld} foo
%{__libtoolize}
%{__make} all
%{__mkdir} -p dir
%{__mv} foo bar
%{__nm} foo
%{__objcopy} foo
%{__objdump} foo
%{__patch} -p1 foo.patch
%{__perl} -pi -e 's/a/b/' foo
%{__python} setup.py build
%{__python2} setup.py build
%{__python3} setup.py build
%{__pypy3} -m pip install
%{__ranlib} libfoo.a
%{__restorecon} -R %{buildroot}
%{__rm} -f foo
%{__rsh} host true
%{__sed} -i s/a/b/ foo
%{__semodule} -i foo.pp
%{__ssh} host true
%{__strip} foo
%{__tar} xf foo.tar
%{__unzip} -o foo.zip
%{__xz} -d foo.xz
%__make all
%__rm -f foo

%files

%changelog
