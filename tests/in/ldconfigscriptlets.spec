%post -n %{libsoname}
/sbin/ldconfig


%postun -n %{libsoname}
/sbin/ldconfig


