Name:           preamble-duplicate-lines
Version:        1.0
Release:        0
Summary:        Duplicate plain lines in the preamble
License:        MIT
# a comment attached to the first duplicate
BuildRequires:  %(rpm -q --queryformat '%{VERSION}' dup)
BuildRequires:  %(rpm -q --queryformat '%{VERSION}' dup)
Requires:       zzz-last
BuildRequires:  %(rpm -q --queryformat '%{VERSION}' other)
BuildRequires:  %(rpm -q --queryformat '%{VERSION}' other)
Requires:       aaa-after

%description
Duplicate plain lines in the preamble.

%changelog
