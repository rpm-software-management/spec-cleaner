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
CFLAGS="%{optflags}" make V=1 %{?_smp_mflags}
CFLAGS="%{optflags}" make V=1 %{?_smp_mflags} eapol_test
CC=gcc CFLAGS='-O2 -g' make
LDFLAGS="-Wl,--as-needed" make VERBOSE=1 all
    V=1 make all
MAKEFLAGS="-k %{?_smp_mflags}" make
CFLAGS="%{optflags} V=1" make
CFLAGS="%{optflags} V=1" make V=1 %{?_smp_mflags} all
FOO=bar make
make %{?_smp_mflags}
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
make all; echo done

%check
CFLAGS="%{optflags}" make V=1 check
make test

%files
%{_bindir}/make-env-prefix

%changelog
