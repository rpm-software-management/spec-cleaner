%build
%if 0%{?suse_version} > 1500
echo suse
%endif
%if 0%{?sles_version}
echo sles
%endif

%changelog
