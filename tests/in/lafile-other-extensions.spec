%install
%make_install
find %{buildroot}%{_datadir}/texmf -name "*.latex" -delete
find %{buildroot} -name "*.lai" -delete
find %{buildroot}%{_datadir} -name '*.layout' -delete
find %{buildroot} -name '*.la*' -delete
find %{buildroot} -name "*.la"|xargs rm -f
