Name:           deprecatedgrep-command-prefixes
Version:        1.0
Release:        0
Summary:        Test egrep and fgrep rewrites after command prefixes
License:        MIT
URL:            https://example.org/
Patch0:         cscope-egrep.out.patch

%description
egrep and fgrep run through xargs, find -exec, sudo, env or a path.

%prep
%autosetup -p1
find . -name "*.h" -print0 | xargs -0 grep -E -l foo
find . -name "*.c" -exec grep -F -l bar {} +

%build
LC_ALL=C grep -E -q foo bar
env LC_ALL=C grep -F -q foo bar
{ grep -E foo bar; }
if /bin/grep -E -q foo bar; then echo found; fi
make EGREP=egrep PREFIX=/opt egrep
echo LC_ALL=C egrep

%install
install -D -m 0755 --target-directory=%{buildroot}/bin %{_bindir}/egrep

%post
sudo grep -E -q foo %{_sysconfdir}/bar || echo missing
%{_bindir}/grep -F -q foo %{_sysconfdir}/bar

%files
/bin/egrep

%changelog
