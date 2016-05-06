%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_bindir}/a

%changelog
