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
cd tests && %make_build check
%make_build check
%make_build check
cd tests && %make_build check
cd tests && CFLAGS="-O2" %make_build check
cd tests && CFLAGS="-O2" %make_build check
echo make all
echo 'run; make V=1 check'
echo "run; make V=1 check"
echo foo\; make check
echo 'x' ; %make_build check
cd tests; cd src && %make_build check
cd tests && %make_build check; V=1 ./verify
echo "a; make all"
echo "a; make all"; %make_build check
%make_build check; ./verify

%files
%{_bindir}/make-midline

%changelog
