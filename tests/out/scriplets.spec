%post -n %{libname} -p /sbin/ldconfig
%post -p /sbin/ldconfig
%post
/sbin/ldconfig
someothercommand

%post -n %{_libname} -p /sbin/ldconfig

%changelog
