%global pkg_name unbrace
%global optflags %{optflags} %{**}
%define typelib typelib-1_0-Unbrace-1_0
Name:           unbrace-value-positions
Version:        1.0
Release:        0
Summary:        Haskell %{pkg_name} library documentation
License:        MIT
URL:            https://example.org/%pkg_name
BuildRequires:  %python_module devel
Requires:       %{pkg_version}foo
Requires:       %{typelib} = %{version}

%description
Haskell %{pkg_name} library documentation files.
Glued %{ghost}foo and %{patch0}2 references stay braced.

%package -n ghc-%pkg_name
Summary:        Haskell %{pkg_name} library development files

%description -n ghc-%pkg_name
Haskell %{pkg_name} library development files.

%build
$CC %{optflags} -D_GNU_SOURCE
perl ./Build.PL optimize="%{optflags}"

%files
%typelib
%ghost/run/unbrace-value-positions

%files -n ghc-%pkg_name
%{_libdir}/libHS%pkg_name.so

%files %{python_files} -f %{name}.lang

%changelog
