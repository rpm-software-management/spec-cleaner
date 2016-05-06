%install
find %{buildroot} -type f -name "*.la" -exec rm -fv {} +
find %{buildroot} -type f -name "*.la" -exec rm -fv {} +
find %{buildroot} -type f -name "*.la" -delete
find %{buildroot} -name *.la -delete
rm %{buildroot}%{_libdir}/*.la

%changelog
