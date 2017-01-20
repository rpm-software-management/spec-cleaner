%define root %version
%if %{?xyz}
%define foobar foobar
%endif
%define complexthing %{root}-complex-%{?foobar}baz
%if %{?abc}
%define ahoj babi
%bcond_without hamster
%endif
%global test somethingelse
%if 0%{?suse_version} > 1230
%bcond_without systemd
%else
%bcond_with    systemd
%endif
%bcond_with self_hosting

%changelog
