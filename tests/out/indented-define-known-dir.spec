#
# A path macro defined inside a conditional is indented, so the pre-scan has to
# strip the indentation before it can see the define. re_bindir then stays off
# and %files keeps its path as written; re_prefix is guarded on _prefix only,
# so the hardcoded /usr inside the define is still rewritten.
#
%if 0%{?sle_version}
  %define _bindir %{_prefix}/bin
%endif
Name:           indented-define-known-dir
Version:        1.0
Release:        0
Summary:        An indented path define has to be seen by the pre-scan
License:        MIT
URL:            https://example.org/indented-define-known-dir

%description
An indented path define has to be seen by the pre-scan.

%files
%{_prefix}/bin/probe

%changelog
