Name:           make-env-prefix
Version:        1.0
Release:        0
Summary:        Test make calls led by variable assignments
License:        MIT
URL:            https://example.org/

%description
make calls led by variable assignments are rewritten to the
make_build macro, while lookalike lines are left alone.

%prep
%autosetup -p1

%build
CFLAGS="%{optflags}" %make_build
CFLAGS="%{optflags}" %make_build eapol_test
CC=gcc CFLAGS='-O2 -g' %make_build
LDFLAGS="-Wl,--as-needed" %make_build all
FOO=bar %make_build
%make_build
CFLAGS = -O2
echo "make all"
echo make all
grep -n make Makefile.in
FOO=bar ninja -C build
FOO=bar
makefile: all
env CFLAGS="-O2" make all
CFLAGS="-O2" make all && ls
CFLAGS="-O2" make all | tee build.log
%make_build all; echo done

%check
CFLAGS="%{optflags}" %make_build check
%make_build test

%files
%{_bindir}/make-env-prefix

%changelog
