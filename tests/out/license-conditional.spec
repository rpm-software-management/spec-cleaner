Name:           licenses
%if 0%{?suse_version}
License:        MIT
%else
License:        MIT AND BSD-3-Clause
%endif

%package devel
Summary:        blabla
License:        GPL-2.0-only

%package nolicense
Summary:        differentblabla

%changelog
