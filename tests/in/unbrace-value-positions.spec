%global pkg_name unbrace
%global optflags %{optflags} %{**}
%define typelib typelib-1_0-Unbrace-1_0

Name:           unbrace-value-positions
Version:        1.0
Release:        1
Summary:        Haskell %{pkg_name} library documentation
License:        MIT
URL:            https://example.org/%{pkg_name}
BuildRequires:  %python_module devel
Requires:       %{typelib} = %{version}
Requires:       %{pkg_version}foo

%description
Haskell %{pkg_name} library documentation files.
Glued %{ghost}foo and %{patch0}2 references stay braced.

%package -n ghc-%{pkg_name}
Summary:        Haskell %{pkg_name} library development files

%description -n ghc-%{pkg_name}
Haskell %{pkg_name} library development files.

%build
$CC ${RPM_OPT_FLAGS} -D_GNU_SOURCE
perl ./Build.PL optimize="$RPM_OPT_FLAGS"

%files
%{typelib}
%{ghost}/run/unbrace-value-positions

%files -n ghc-%{pkg_name}
%{_libdir}/libHS%{pkg_name}.so

%files %{python_files} -f %{name}.lang
