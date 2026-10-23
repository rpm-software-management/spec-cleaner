#
# Path macroisation rewrites literal paths to %{...} macros in the full run;
# the minimal run keeps every path as written. The lines below carry the
# shapes the Factory corpus showed being rewritten: %description prose,
# %define values, a path-valued tag, scriptlets, an indented comment and
# %files entries. $RPM_BUILD_ROOT is a variable substitution rather than a
# path macroisation and is rewritten in both modes.
#
%define CATALINA_HOME %{_datadir}/tomcat6
%define apparmor_bin_prefix %{_prefix}/lib/apparmor
Name:           path-macroisation
Version:        1.0
Release:        0
Summary:        Paths stay as written in the minimal run
License:        MIT
URL:            https://example.org/path-macroisation
BuildRequires:  %{_bindir}/make

%description
The driver is %{_bindir}/hpijs from HPLIP.
It uses the %{apparmor_profilesdir}/ directory structure.

%install
install -D -m 0644 foo.conf %{buildroot}%{_datadir}/foo/foo.conf
install -D -m 0755 foo %{_bindir}/foo

%post
    # the cache lives in %{_localstatedir}/cache/apparmor these days
    echo "%ghost %config %{apparmor_profilesdir}/local/$oldlocal"

%files
%{_datadir}/foo/foo.txt
%dir %{apparmor_profilesdir}

%changelog
