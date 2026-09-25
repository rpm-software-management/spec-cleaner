Name:           description-whitespace-lines
Version:        1.0
Release:        0
Summary:        Whitespace-only lines in the description
License:        MIT

%description
First paragraph.

Second paragraph.

Third paragraph.

%prep
%setup -q

%build
%make_build

%install
%make_install

%files
%license COPYING

%changelog
