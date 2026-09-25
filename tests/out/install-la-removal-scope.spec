%install
%make_install
rm -f %{buildroot}%{_libdir}/libfoo.so %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_libdir}/pkgconfig %{buildroot}%{_libdir}/*.la
rm -f foo %{buildroot}%{_libdir}/*.la
make install DESTDIR=%{buildroot} && rm -f %{buildroot}%{_libdir}/*.la
find %{buildroot} -type f -name "*.la" -delete -print
find %{buildroot} -name '*.la' -exec sed -i "s|-L%{_builddir}[^ ]*||g" {} \;
find %{buildroot} -type f -name '*.la' -exec chmod 644 {} +
find %{buildroot}%{_libdir} -name "*.la" -print
find %{buildroot} -name '*.la' | xargs sed -i 's|^dependency_libs=.*|dependency_libs=|'
find %{buildroot} -type f -name "*.la" -delete -print
find %{buildroot} -type f -name "*.la" -delete -print
find %{buildroot} -name '*.la' -exec rm {} \; -o -print

%changelog
