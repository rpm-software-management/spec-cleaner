# A pattern() mention outside a condition must not move the next %if block
Name:           pattern-latch
Version:        1.0
Release:        0
Summary:        Test package mentioning pattern() in a tag
License:        MIT
URL:            https://example.org/pattern-latch
BuildRequires:  foo
%if 0%{?suse_version}
BuildRequires:  bar
%endif

%description
Test package.

%changelog
