Name:           foo
Version:        1.0
Release:        0
Summary:        Foo
License:        MIT
URL:            https://example.org
Source0:        foo.tar.gz

%sourcelist
https://example.org/foo-extra-%{version}.tar.gz
bar.tar.gz

%patchlist
zzz.patch
aaa.patch

%description
Foo.

%prep
%setup -q

%generate_buildrequires
echo 'pkgconfig(zlib)'

%conf
%configure

%build
%make_build

%install
%make_install

%files
%{_bindir}/foo

%changelog
