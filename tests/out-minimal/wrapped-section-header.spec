Name:           wrapped-section-header
Version:        1.0
Release:        0
Summary:        Test section headers wrapped in conditionals
License:        MIT
URL:            https://example.org/

%description
Test.

%package doc
Summary:        Documentation

%description doc
Documentation.

%if 0%{?with_build}
%build
%endif
./configure
make

%if 0%{?suse_version} >= 1600
%post
%else
%post -n other
%endif
%service_add_post foo.service
/sbin/ldconfig

%if 0%{?suse_version} >= 1600
%files
%defattr(0644,root,root,0755)
%else
%files -f %{name}.lang
%endif
%defattr(-,root,root,-)
%license COPYING
%{_mandir}/man1/foo.1.*
%ifarch s390x
%{_bindir}/foo-s390
%endif
%if 0%{?with_extra}
%{_bindir}/foo-extra
%endif

%files doc
%if 0%{?with_html}
%doc html
%if 0%{?with_api}
%files -n api
%endif
%elif 0%{?with_pdf}
%defattr(-,root,root)
%{_mandir}/man8/foo.8.*
%endif

%if 0%{?with_main}
%files -n main
%{_bindir}/main
%ifarch x86_64
%{_bindir}/main-x86
%endif
%else
%define other_name other
Requires:       other
%endif

%changelog
