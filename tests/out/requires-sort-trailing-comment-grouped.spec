Name:           requires-sort-trailing-comment-grouped
Version:        1.0
Release:        0
Summary:        Sort class ignores trailing comments on grouped token lines
License:        MIT
URL:            https://example.com
Requires:       aaa
# pinned, see perl(Bar) docs
Requires:       zzz # uses perl(Bar)
Requires:       perl(Bar)

%description
A plain dep grouped with a preceding comment line, whose trailing
comment mentions perl(), must sort with the plain deps, not with
the brackety deps.

%changelog
