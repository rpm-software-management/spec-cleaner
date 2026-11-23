#
# printf-like format strings of other tools carry %-directives that
# belong to the tool, not to rpm: printf/sprintf (shell builtin,
# /usr/bin/printf, perl/ruby, awk), date(1) '+FORMAT' (strftime),
# stat(1) -c/--format, and git log --format/--pretty/--date=format:.
# The brace-the-macros pass must leave them alone. A bare macro
# outside a format string is still braced.
#
Name:           format-strings
Version:        1.0
Release:        0
Summary:        printf-like format strings stay unbraced
License:        MIT
URL:            https://example.org/format-strings

%description
printf-like format strings stay unbraced.

%build
printf "%s\n%s" "$MIN_TIME_VERSION" "$MIN_PG_VERSION"
printf "%d%02d" $maj $min
printf '%s' "6-zig-..."
printf -- "%s\n" foo
printf -v var "%s\n"
sprintf "%s" $x
printf "%+d" $x
awk -F. '{ printf "%d.%03d%03d", $1, $2, $3 }'
date +%Y-%m-%d
date "+%s"
date -u -d "..." "+%s"
date -r LICENSE +%s
date '+%Y%m%d'
date -u '+%FT%T%z'
date --date=@... +'\\date{%B %Y}'
date -u +%Y-%m-%dT%H:%M:%SZ
date --date="$..." '+%%F %T%z'
date -r %{SOURCE1} "+%B %d, %Y"
stat -c '%G' /usr/bin/foo
stat -c "%a" /usr/bin/foo
stat -c %Y /usr/bin/foo
stat --format="%y" /usr/bin/foo
stat -c %U:%G:%a /usr/bin/foo
stat -L -c "%i" /usr/bin/foo
stat --format=%Y /usr/bin/foo
%define git_version %(git log '-n1' '--date=format:%Y%m%d' '--no-show-signature' "--pretty=format:+git%cd.%h")
printf "%s\n" /usr/share/foo
date +%Y-%m-%d /usr/share/foo
stat -c %a /usr/share/foo
test "$(stat --format=%a %{buildroot}%{_bindir}/git)" = 755
printf "Date: $(date "+%F") %name\n"
git log -1 --date=format:"+%Y" --format=%cd

%files
%license LICENSE

%changelog
