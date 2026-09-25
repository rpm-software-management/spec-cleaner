Name:           deprecatedgrep-paths
Version:        1.0
Release:        0
Summary:        Test that egrep and fgrep are only rewritten as commands
License:        MIT
URL:            https://example.org/
Patch0:         grep-egrep-warning.patch
Requires:       fgrep-compat
Provides:       egrep = %{version}
Provides:       fgrep

%description
egrep and fgrep are provided as symlinks.

%prep
egrep -rl foo . ; fgrep -l bar file

%build
if ! egrep -q "^foo" users.txt; then echo missing; fi
cat build.log | fgrep -v warning

%install
ln -s grep %{buildroot}%{_bindir}/egrep
ln -s grep %{buildroot}%{_bindir}/fgrep
for f in egrep fgrep; do echo $f; done

%post
egrep -q foo users.txt || echo missing

%files
%{_bindir}/egrep
%{_bindir}/fgrep
%{_mandir}/man1/egrep.1%{?ext_man}

%changelog
