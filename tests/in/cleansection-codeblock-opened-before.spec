### COMMON-install-BEGIN ###
%install
make install

%clean
rm -rf %{buildroot}
### COMMON-install-END ###

%files
%{_bindir}/main

%check
make check
# MANUAL BEGIN
%clean
rm -rf %{buildroot}
# MANUAL END

%files sub
%{_bindir}/sub

%check
make test
# SECTION old distros
%clean
# SECTION remove the buildroot
rm -rf %{buildroot}
# /SECTION
# /SECTION

%files other
%{_bindir}/other

%changelog
