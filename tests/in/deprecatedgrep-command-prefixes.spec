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
find . -name "*.h" -print0 | xargs -0 egrep -l foo
find . -name "*.c" -exec fgrep -l bar {} +

%build
LC_ALL=C egrep -q foo bar
env LC_ALL=C fgrep -q foo bar
{ egrep foo bar; }
if /bin/egrep -q foo bar; then echo found; fi
make EGREP=egrep PREFIX=/opt egrep
echo LC_ALL=C egrep

%install
install -D -m 0755 --target-directory=%{buildroot}/bin /usr/bin/egrep

%post
sudo egrep -q foo /etc/bar || echo missing
%{_bindir}/fgrep -q foo /etc/bar

%files
/bin/egrep

%changelog
