%post -n %libname -p /sbin/ldconfig

%post
/sbin/ldconfig

%post
/sbin/ldconfig
someothercommand

%post -n %{_libname}
/sbin/ldconfig