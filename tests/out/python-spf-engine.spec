#
# spec file for package python-spf-engine
#
# Copyright (c) 2025 Ákos Szőts <szotsaki@gmail.com>
# Copyright (c) 2020 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

# Trick python_subpackages not to change it to python3 string
%define policyd_spf python-policyd-spf
%define oname python
%if 0%{?suse_version} > 1500
%bcond_without libalternatives
%else
%bcond_with libalternatives
%endif
Name:           python-spf-engine
Version:        3.1.0
Release:        0
Summary:        SPF (Sender Policy Framework) processing engine for Postfix
License:        Apache-2.0 AND GPL-2.0-only
Group:          Development/Languages/Python
URL:            https://launchpad.net/spf-engine
Source:         https://files.pythonhosted.org/packages/source/s/spf-engine/spf-engine-%{version}.tar.gz
BuildRequires:  %{python_module flit-core >= 3.8}
BuildRequires:  %{python_module pip}
BuildRequires:  fdupes
BuildRequires:  python-rpm-macros
Requires:       python-authres
Requires:       python-pyspf
Suggests:       python-pymilter
Conflicts:      %{policyd_spf}
Obsoletes:      %{policyd_spf} < 2
Provides:       %{policyd_spf} = %{version}
Provides:       %{oname}-spf-engine = %{version}
BuildArch:      noarch
%if %{with libalternatives}
BuildRequires:  alts
Requires:       alts
%else
Requires(post): update-alternatives
Requires(postun): update-alternatives
%endif
%python_subpackages

%description
SPF (Sender Policy Framework) backend for pypolicyd-spf.

Provides a back-end to support SPF integration with Postfix and Sendmail using both the Postfix policy service and the Sendmail milter protocol.

%prep
%autosetup -p1 -n spf-engine-%{version}

# Remove shebang from Python library
sed -i '/^#!/d' spf_engine/*.py

%build
%pyproject_wheel

%install
%pyproject_install
%python_clone -a %{buildroot}%{_bindir}/policyd-spf
%python_clone -a %{buildroot}%{_bindir}/pyspf-milter
%python_group_libalternatives policyd-spf pyspf-milter

cp -r --no-dereference --link %{buildroot}%{_prefix}%{_sysconfdir} %{buildroot}
rm -r %{buildroot}%{_prefix}%{_sysconfdir}

mkdir -p %{buildroot}%{_docdir}/%{policyd_spf}
mv -v %{buildroot}%{_datadir}/doc/%{policyd_spf}/* %{buildroot}%{_docdir}/%{policyd_spf}/

rm %{buildroot}%{_initddir}/pyspf-milter

mkdir -p %{buildroot}%{_sbindir}
ln -s %{_sbindir}/service %{buildroot}%{_sbindir}/rcpyspf-milter

%python_expand %fdupes %{buildroot}%{$python_sitelib}

%pre
%python_libalternatives_reset_alternative policyd-spf
%python_libalternatives_reset_alternative pyspf-milter
%service_add_pre pyspf-milter.service

%post
%python_install_alternative policyd-spf
%python_install_alternative pyspf-milter
%service_add_post pyspf-milter.service

%preun
%service_del_preun pyspf-milter.service

%postun
%python_uninstall_alternative policyd-spf
%python_uninstall_alternative pyspf-milter
%service_del_postun pyspf-milter.service

%files %{python_files}
%doc CHANGES README.txt
%dir %{_docdir}/%{policyd_spf}
%doc %{_docdir}/%{policyd_spf}/README.per_user_whitelisting
%{_mandir}/*/*
%license COPYING

%python_alternative %{_bindir}/policyd-spf
%python_alternative %{_bindir}/pyspf-milter

%{python_sitelib}/spf_engine
%{python_sitelib}/spf_engine-%{version}.dist-info

%dir %{_sysconfdir}/%{policyd_spf}
%config(noreplace) %{_sysconfdir}/%{policyd_spf}/policyd-spf.conf
%config %{_sysconfdir}/%{policyd_spf}/policyd-spf.conf.commented

%dir %{_sysconfdir}/pyspf-milter
%config(noreplace) %{_sysconfdir}/pyspf-milter/pyspf-milter.conf

%{_prefix}/lib/systemd/system/pyspf-milter.service
%{_sbindir}/rcpyspf-milter

%changelog
