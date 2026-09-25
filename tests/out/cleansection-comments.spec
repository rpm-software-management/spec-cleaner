%install
%make_install

# Main package: keep /x owned here, see bsc#123
%files
/x

%files sub
%{_bindir}/sub

%if 0%{?suse_version} > 1500
# only on new distributions
%files extra
%{_bindir}/extra
%endif

%changelog
