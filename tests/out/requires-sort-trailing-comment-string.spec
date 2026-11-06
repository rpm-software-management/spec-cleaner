Name:           requires-sort-trailing-comment-string
Version:        1.0
Release:        0
Summary:        Sort class ignores trailing comments on string-kept lines
License:        MIT
URL:            https://example.com
Requires:       aaa
# version pinned to the installed glibc
Requires:       zzz %(rpm -q --queryformat '%{VERSION}' glibc) # uses perl(Bar)
Requires:       perl(Bar)

%description
A string-kept dep (an rpm call) whose trailing comment mentions
perl() must sort with the plain deps, not with the brackety deps.

%changelog
