Name:           section-headers-without-blank-line
Version:        1.0
Release:        0
Summary:        Recognise section headers that directly follow the previous section
License:        MIT
URL:            https://example.org
Source0:        foo.tar.gz

%patchlist
zzz.patch
aaa.patch

%description
Section headers without a blank line before them still start a new section.

%prep
%setup -q

%generate_buildrequires
echo 'pkgconfig(zlib)'

%conf
# FIXME: you should use the %%configure macro
./configure --prefix=%{_prefix}

%build
%make_build

%install
%make_install

%files
%{_bindir}/foo

%triggerin -- bash
    echo "a  b"

%triggerprein -- baz
    echo "x  y"

%changelog
