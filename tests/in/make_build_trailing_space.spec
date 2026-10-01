Name:           test
Version:        1.0
Release:        0
Summary:        test
License:        MIT
Group:          test

%description
test

%build
make  %{?_smp_mflags}
make   VERBOSE=1 %{?_smp_mflags}
make  V=1
make V=10 %{?_smp_mflags}

%changelog
