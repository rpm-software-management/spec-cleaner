Name:           sourceorder-stanzas
Version:        1.0
Release:        0
Summary:        Stanzas keep their written order in minimal mode
License:        MIT

%files
%{_bindir}/sourceorder-stanzas

%description
The files list is written before this description and before the prep
section; all three stanzas stay in the order they were written in.

%prep
%setup -q

%changelog
