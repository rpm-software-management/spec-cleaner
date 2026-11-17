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
# A new statement after a continued BuildRequires is not the fragment:
# its own path macroises as usual. And a trailing comment on a
# path-valued BuildRequires is not part of the dependency, so the paths
# in it macroise as usual while the value stays literal.
#
%define CATALINA_HOME /usr/share/tomcat6
%define apparmor_bin_prefix /usr/lib/apparmor
Name:           path-macroisation
Version:        1.0
Release:        0
Summary:        Paths stay as written in the minimal run
License:        MIT
URL:            https://example.org/path-macroisation
BuildRequires:  /usr/bin/make
BuildRequires:  (/usr/bin/foo or bar)
BuildRequires:  foo
BuildRequires:  /usr/bin/bar
%{?with_foo:BuildRequires: /usr/bin/foo}
#!BuildRequires: /usr/bin/foo
#!BuildRequires: foo /usr/bin/bar
%{?with_foo:#!BuildRequires: /usr/bin/foo}
%{?with_foo:BuildRequires: foo /usr/bin/bar}
%{?with_foo:#!BuildRequires: foo /usr/bin/bar}
BuildRequires:  qux
Requires:       /usr/bin/bar
BuildRequires:  /usr/bin/gpg # see /usr/bin/bar for details

%description
The driver is /usr/bin/hpijs from HPLIP.
It uses the /etc/apparmor.d/ directory structure.

%install
install -D -m 0644 foo.conf %{buildroot}/usr/share/foo/foo.conf
install -D -m 0755 foo /usr/bin/foo

%post
    # the cache lives in /var/cache/apparmor these days
    echo "%ghost %config /etc/apparmor.d/local/$oldlocal"

%files
/usr/share/foo/foo.txt
%dir /etc/apparmor.d

%changelog
