Name:           make-midline
Version:        1.0
Release:        0
Summary:        Test make calls after another command or with a path
License:        MIT
URL:            https://example.org/

%description
Test that make calls led by another command or an absolute
path are rewritten to the make_build macro.

%prep
%autosetup -p1

%check
cd tests && make check
/usr/bin/make check
make check
cd tests && make check %{?_smp_mflags}
cd tests && CFLAGS="-O2" make check
cd tests && CFLAGS="-O2" make check %{?_smp_mflags}
echo make all
echo 'run; make V=1 check'
echo "run; make V=1 check"
echo foo\; make check
echo 'x' ; make check
cd tests; cd src && make check
cd tests && make check; V=1 ./verify
make check V=1; ./verify

%files
%{_bindir}/make-midline

%changelog
