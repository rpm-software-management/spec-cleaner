Name:           sourceorder-duplicate
Version:        1.0
Release:        0
Summary:        Merged duplicate group keeps its written position in minimal mode
License:        MIT
# a comment attached to the first duplicate
BuildRequires:  %(rpm -q --queryformat '%{VERSION}' dup)
BuildRequires:  %(rpm -q --queryformat '%{VERSION}' dup)
Requires:       zzz-last

%description
The duplicate BuildRequires group above is merged into one line; the
merged group stays where it was written and the Requires line that
followed it stays after it.

%files
%{_bindir}/sourceorder-duplicate

%changelog
