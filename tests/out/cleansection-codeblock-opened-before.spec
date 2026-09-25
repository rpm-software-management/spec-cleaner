### COMMON-install-BEGIN ###
%install
%make_install

### COMMON-install-END ###

%files
%{_bindir}/main

%check
%make_build check
# MANUAL BEGIN
# MANUAL END

%files sub
%{_bindir}/sub

%check
%make_build test
# SECTION old distros
# /SECTION

%files other
%{_bindir}/other

%changelog
