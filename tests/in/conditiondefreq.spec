%if xxx
%define something xxx
%else
%define something yyy
%endif
Name: something
Version: something
%if %something
%define something2 xxx
%else
%define something2 yyy
%endif
BuildRequires: something
%if %something2
Requires: ddd
%endif
%if %something2
BuildRequires: variable
%define crazystuff value
%endif
