# '%%' is the rpm escape for a literal percent sign, so '%%{license}'
# is not a macro invocation and must be left alone (gh#315)
%global ipxe_license %(rpm -q --qf %%{license} %{ipxe})
# while a plain '%{license}' is still unbraced as usual
%global plain_license %license
Name:           ipxe
Version:        1.0
Release:        0
Summary:        Test
License:        GPL-2.0-or-later
Source0:        ipxe-%{version}.tar.gz

%description
Test.

%changelog
