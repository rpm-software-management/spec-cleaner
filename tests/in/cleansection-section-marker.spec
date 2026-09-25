%install
make install
%if 0%{?suse_version} < 1500
%clean
# SECTION remove the buildroot
rm -rf %{buildroot}
%endif

%files
%{_bindir}/main

%clean
# SECTION remove the buildroot
rm -rf %{buildroot}
# /SECTION
rm -rf %{_tmppath}

%files sub
%{_bindir}/sub

%changelog
