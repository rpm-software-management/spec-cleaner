Name:           macro-space-paren
Version:        1.0
Release:        0
Summary:        Test %{name} (a library)
License:        MIT
URL:            https://example.org/
%if (0%{?suse_version} > 1500)
BuildRequires:  pkgconfig(new)
%elif (0%{?suse_version} > 1300)
BuildRequires:  pkgconfig(old)
%endif

%description
This package provides %{name} (a library for foo).

%build
echo %{version} (release %{release})

%install
%python_expand (cd build; $python setup.py install)

%files
%lang (de) %{_datadir}/locale/de/foo.mo
%attr (0755,root,root) %{_bindir}/foo
%config (noreplace) %{_sysconfdir}/foo.conf
%verify (not md5) %{_sysconfdir}/foo.state
%caps (cap_net_raw=p) %{_bindir}/foo-ping
%dev (c, 1, 3) /dev/foo

%changelog
