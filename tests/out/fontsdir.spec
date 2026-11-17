#
# %{_fontsdir} is only defined when fontpackages-devel is installed, so
# rewriting /usr/share/fonts to it forces a BuildRequires the spec never
# needed. Full mode must leave the fonts path alone: it macroises only
# as far as %{_datadir}, which is a base macro.
#
Name:           fontsdir
Version:        1.0
Release:        0
Summary:        Fonts paths stay literal, never %{_fontsdir}
License:        MIT
URL:            https://example.org/fontsdir

%description
Fonts paths stay literal, never %{_fontsdir}.

%build
%configure \
	   --with-test-font-path=%{_datadir}/fonts/truetype/DejaVuSans.ttf
%make_build

%install
install -D -m 0644 %{name}.ttf %{buildroot}%{_datadir}/fonts/%{name}.ttf

%files
%dir %{_datadir}/fonts
%{_datadir}/fonts/%{name}.ttf

%changelog
