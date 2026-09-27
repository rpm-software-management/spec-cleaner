%clean
%if 0%{?a}
rm -rf %{buildroot}
%endif
%else
%files
/x

%changelog
