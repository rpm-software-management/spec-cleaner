#
# spec file for package spec-cleaner
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
# Copyright (c) 2012 Vincent Untz <vuntz@opensuse.org>
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

Name:           spec-cleaner
Version:        0.4.1
Release:        0
%debug_package
Summary:        .spec file cleaner
License:        BSD-3-Clause
Group:          Development/Tools/Other
Url:            http://github.com/openSUSE/spec-cleaner
Source0:        https://github.com/openSUSE/%{name}/archive/%{name}-%{version}.tar.gz
BuildRequires:  python
%if 0%{?suse_version} > 01220
BuildRequires:  python3
%endif
Requires:       python-base
Provides:       obs-service-format_spec_file = %{version}
Obsoletes:      obs-service-format_spec_file < %{version}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%{debug_package}

%description
This script cleans spec file according to some arbitrary style guide. The
results it produces should always be checked by someone since it is not and
will never be perfect.

%debug_package

%prep
%setup -q -n %{name}-%{name}-%{version}

%build

%check
# Fails for now, uncomment with next release
#make check -j1

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags} \
	LIBEXECDIR=%{_libexecdir} \
	LIBDIR=%{_libdir} \
	SITEDIR=%{python_sitelib} \

%files
%defattr(-, root, root)
%{_bindir}/%{name}
%dir %{_libexecdir}/obs/
%dir %{_libexecdir}/obs/service/
%{_libexecdir}/obs/service/format_spec_file
%{_libexecdir}/obs/service/format_spec_file.service
%dir %{python_sitelib}/spec_cleaner/
%{python_sitelib}/spec_cleaner/__init__.py*
%{python_sitelib}/spec_cleaner/fileutils.py*
%{python_sitelib}/spec_cleaner/rpmbuild.py*
%{python_sitelib}/spec_cleaner/rpmcheck.py*
%{python_sitelib}/spec_cleaner/rpmcleaner.py*
%{python_sitelib}/spec_cleaner/rpmcopyright.py*
%{python_sitelib}/spec_cleaner/rpmdescription.py*
%{python_sitelib}/spec_cleaner/rpmexception.py*
%{python_sitelib}/spec_cleaner/rpmfiles.py*
%{python_sitelib}/spec_cleaner/rpminstall.py*
%{python_sitelib}/spec_cleaner/rpmpreamble.py*
%{python_sitelib}/spec_cleaner/rpmprep.py*
%{python_sitelib}/spec_cleaner/rpmprune.py*
%{python_sitelib}/spec_cleaner/rpmregexp.py*
%{python_sitelib}/spec_cleaner/rpmscriplets.py*
%{python_sitelib}/spec_cleaner/rpmsection.py*
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/excludes-bracketing.txt
%{_datadir}/%{name}/licenses_changes.txt
%{_datadir}/%{name}/pkgconfig_conversions.txt

%changelog
