#
# Path macroisation rewrites literal paths to %{...} macros in the full run;
# the minimal run keeps every path as written. The lines below carry the
# shapes the Factory corpus showed being rewritten: %description prose,
# %define values, a path-valued tag, scriptlets, an indented comment and
# %files entries. $RPM_BUILD_ROOT is a variable substitution rather than a
# path macroisation and is rewritten in both modes.
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
