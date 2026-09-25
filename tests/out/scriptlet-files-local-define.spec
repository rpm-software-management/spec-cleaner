Name:           foo
Version:        1.0
Release:        0
Summary:        Foo
License:        MIT

%description
Foo.

%post
%global svc foo.service
%if 0%{?suse_version}
%service_add_post %{svc}
%endif
echo done

%files
%define mydocs %{_docdir}/foo
%if 0%{?suse_version}
%{_bindir}/a
%endif
%{_bindir}/b
%{mydocs}

%changelog
