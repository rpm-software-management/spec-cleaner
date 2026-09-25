%install
%make_install
%if 0%{?suse_version} < 1500
%endif

%files
%{_bindir}/main

%files sub
%{_bindir}/sub

%changelog
