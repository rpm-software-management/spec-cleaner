#
# Path macroisation rewrites literal paths to %{...} macros in the full run;
# the minimal run keeps every path as written. The lines below carry the
# shapes the Factory corpus showed being rewritten: %description prose,
# %define values, a path-valued tag, scriptlets, an indented comment and
# %files entries. $RPM_BUILD_ROOT is a variable substitution rather than a
# path macroisation and is rewritten in both modes. A path-valued
# BuildRequires stays literal in both modes: the OBS scheduler records
# BuildRequires unexpanded, so a macroised file dependency matches nothing.
# That holds for the tag in a rich dependency, a backslash-continued
# dependency and a one-line conditional, too, and for the dep pragma form
# (#!BuildRequires:), whose continuation fragment and one-line conditional
# carry the same file dependency. A one-line conditional whose value
# continues onto the next line joins the same way, pragma form included.
#
%define CATALINA_HOME %{_datadir}/tomcat6
%define apparmor_bin_prefix %{_prefix}/lib/apparmor
%{?with_foo:#!BuildRequires: /usr/bin/foo}
%{?with_foo:#!BuildRequires: foo /usr/bin/bar}
Name:           path-macroisation
Version:        1.0
Release:        0
Summary:        Paths stay as written in the minimal run
License:        MIT
URL:            https://example.org/path-macroisation
BuildRequires:  (/usr/bin/foo or bar)
BuildRequires:  /usr/bin/bar
BuildRequires:  /usr/bin/foo
BuildRequires:  /usr/bin/make
BuildRequires:  foo
%{?with_foo:BuildRequires: /usr/bin/foo}
%{?with_foo:BuildRequires: foo /usr/bin/bar}

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
