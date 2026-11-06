%build
%bcond_with foo
make %{?_smp_mflags}
%if %{with foo}
make foo
%endif
make bar
