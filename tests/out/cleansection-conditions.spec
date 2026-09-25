%install
%make_install

%files
%{_bindir}/main

%if 0%{?suse_version} > 1500
%files sub
%{_bindir}/sub
%endif

%changelog
