%install
mkdir -p %{buildroot}%{_datadir}/foo

%check
true

%clean

rm -rf %{buildroot}

%files
%{_datadir}/foo

%clean
rm -rf %{_builddir}/tmpdata

rm -rf %{buildroot}

%files sub
%{_bindir}/sub

%clean

%{__rm} -rf %{buildroot}

%files extra
%{_bindir}/extra

%clean
%if 0%{?suse_version}

rm -rf %{buildroot}
%endif

# kept above the next package
%files more
%{_bindir}/more
