#
# find -printf format strings carry %-directives that belong to find,
# not to rpm: %f is the basename, %p the path, %h the directory. The
# brace-the-macros pass must leave them alone, or the build fails when
# GNU find rejects the braced form (%{ is reserved for future use).
# The same holds for -fprintf and for stat --printf. A bare macro
# outside a format string is still braced. The format may also be
# unquoted (-printf %p, --printf=%a, -c%a); the format then runs to
# the next shell separator.
#
Name:           find-printf
Version:        1.0
Release:        0
Summary:        find -printf directives stay unbraced
License:        MIT
URL:            https://example.org/find-printf

%description
find -printf directives stay unbraced.

%install
find %{buildroot}%{_mandir}/man8 -regextype posix-extended \
  -regex ".*(linux32|linux64)\\.8.*" \
  -printf "%{_mandir}/man8/%f*\n" >> %{name}.files
find %{buildroot}%{_bindir}/ -regextype posix-extended -type l \
  -regex ".*(linux32|linux64)$" \
  -printf "%{_bindir}/%f\n" >> %{name}.files
find . -xtype l -delete -printf "deleted '%f'\n"
find * -name \*.so -printf "/%p\n"
find $root -name FEATURE -printf ' -I%h'
find -type l -printf '%f\a%l\n'
find . -type f -fprintf /tmp/out.txt "%p %s\n"
find . -type f -printf %p\n
find . -type f -fprintf f %p\n
stat --printf=%a /var/spool/mail/
stat -c%a /var/spool/mail/
test 1777 = "$(stat --printf='%a' /var/spool/mail/)" || exit 1
install -D -m 0644 foo.conf %buildroot/usr/share/foo/foo.conf

%files
%license LICENSE

%changelog
