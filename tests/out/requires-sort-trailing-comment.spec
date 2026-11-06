Name:           requires-sort-trailing-comment
Version:        1.0
Release:        0
Summary:        Sort class ignores trailing comments
License:        MIT
URL:            https://example.com
Requires:       aaa
Requires:       zzz # uses perl(Bar)
Requires:       perl(Bar)

%description
A plain dep whose trailing comment mentions perl() must
sort with the plain deps, not with the brackety deps.

%changelog
