Name:           description-authors-after-macro
Version:        1.0
Release:        0
Summary:        Authors block after a macro line
License:        MIT

%description
%{name} is a tool for testing.

Authors:
--------
    John Doe <john@example.com>

%prep
%setup -q

%build
%make_build

%install
%make_install

%files
%license COPYING

%changelog
