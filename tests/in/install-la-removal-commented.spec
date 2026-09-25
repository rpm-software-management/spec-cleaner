%install
%make_install
# the plugin loader needs the .la files, keep them
#rm -f %{buildroot}%{_libdir}/*.la
# find %{buildroot} -name "*.la" -delete
  #find %{buildroot} -type f -name "*.la" -delete -print
rm -f %{buildroot}%{_libdir}/*.la
