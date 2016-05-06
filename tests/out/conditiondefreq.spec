%if xxx
%define something xxx
%else
%define something yyy
%endif
%if %{something}
%define something2 xxx
%else
%define something2 yyy
%endif
%if %{something2}
%define crazystuff value
BuildRequires:  variable
%endif
Name:           something
Version:        something
BuildRequires:  something
%if %{something2}
Requires:       ddd
%endif

%changelog
