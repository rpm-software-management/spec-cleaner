%define selfconflict() %1
%define plainmacro plainvalue
Name:           depmacroargs
Version:        1.0
Release:        0
Summary:        Dependency lines carrying macro arguments
License:        GPL-2.0-only
BuildRequires:  pkg1
BuildRequires:  pkg3
BuildRequires:  pkg2
Requires:       %plainmacro
Requires:       foo
Conflicts:      %selfconflict libgcc_s%{libgcc_s}
Conflicts:      %selfconflict libgcc_s%{libgcc_s}-32bit
Conflicts:      %selfconflict liba libb
Conflicts:      %selfconflict liba
Conflicts:      %selfconflict libb

%description
Dependency lines carrying macro arguments.

%changelog
