Name:           foo
Version:        1.0
Release:        0
Summary:        Foo
License:        GPL-2.0-or-later
URL:            https://example.com
Source0:        foo-1.0.tar.gz

%description
Foo.

%define sover 1
%package -n libfoo%{sover}
Summary:        Library
License:        LGPL-2.1-or-later

%description -n libfoo%{sover}
Library.

%prep
%setup -q

%build

%install

%files
%license COPYING

%global docdir %{_docdir}/foo
%files -n libfoo%{sover}

%bcond_with foo
%changelog
