%install
%make_install
rm -f %{buildroot}%{_libdir}/libfoo.so %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_libdir}/pkgconfig %{buildroot}%{_libdir}/*.la
rm -f foo %{buildroot}%{_libdir}/*.la
make install DESTDIR=%{buildroot} && rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/*.la %{buildroot}%{_libdir}/sox/*.la
find %{buildroot} -name '*.la' -exec sed -i "s|-L%{_builddir}[^ ]*||g" {} \;
find %{buildroot} -type f -name '*.la' -exec chmod 644 {} +
find %{buildroot}%{_libdir} -name "*.la" -print
find %{buildroot} -name '*.la' | xargs sed -i 's|^dependency_libs=.*|dependency_libs=|'
find %{buildroot} -name '*.la' -exec rm -f {} \;
find %{buildroot} -name '*.la' -print0 | xargs -r0 rm -fv
find %{buildroot} -name '*.la' -exec rm {} \; -o -print
