#
# The program argument of awk(1) carries %-forms that belong to awk,
# not to rpm: regex literals matching spec text like %lang(...),
# printf formats, strftime formats. The brace-the-macros pass must
# leave them alone. A bare macro outside the program is still braced.
#
Name:           awk-lang
Version:        1.0
Release:        0
Summary:        awk program arguments keep their %-forms
License:        MIT
URL:            https://example.org/awk-lang

%description
Awk program arguments keep their %-forms.

%install
awk -v P=%{buildroot} '/^(%lang|[^%])/{print P $NF}' libpq.files libecpg.files | xargs rm
awk -F. '{ printf "%d.%03d%03d", $1, $2, $3 }'
gawk '/^(%lang|[^%])/{print}' file
awk -F '[<>]' '/%lang/{print}'
awk '/%lang/{print}' %{_datadir}/foo

%changelog
