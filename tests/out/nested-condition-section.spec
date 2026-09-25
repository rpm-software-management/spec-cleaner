Name:           foo
Version:        1.0
Release:        0
Summary:        Foo
License:        MIT
Source:         foo.tar.gz
BuildRequires:  gcc
%if %{with extras}
%ifarch x86_64
%package extras
Summary:        Extras

%description extras
Extras.
%endif
%endif

%description
Foo.

%package -n libfoo1
Summary:        Library
%if %{with a}
%ifarch x86_64
Requires:       bar

%description -n libfoo1
Library.
%endif
%endif

%package devel
Summary:        Devel
%if %{with a}
Requires:       baz

%description devel
Devel.
%endif

%changelog
