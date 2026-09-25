%install
make install

%clean
rm -rf %{buildroot}
# Main package: keep /x owned here, see bsc#123
%files
/x

%clean
# clean it
rm -rf %{buildroot}
#rm -rf %{_tmppath}

%files sub
%{_bindir}/sub

%clean
rm -rf %{buildroot}
%if 0%{?suse_version} > 1500
# only on new distributions
%files extra
%{_bindir}/extra
%endif
