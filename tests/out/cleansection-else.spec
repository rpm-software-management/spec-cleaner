%install
%make_install

%if 0%{?suse_version}
%else
%files
%{_bindir}/main
%endif

%changelog
