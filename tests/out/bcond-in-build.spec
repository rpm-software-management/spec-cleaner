%build
%bcond_with foo
%make_build
%if %{with foo}
%make_build foo
%endif
%make_build bar

%changelog
