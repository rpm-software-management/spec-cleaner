Name:           make_build_double_space
Version:        1.0
Release:        0
Summary:        Test double space before smp_mflags
License:        MIT
Group:          Development/Tools/Building

%description
Test that 'make  %%{?_smp_mflags}' (two spaces) becomes '%%make_build'
without trailing whitespace. Also test with VERBOSE=1.

%prep

%build
make  %{?_smp_mflags}
make  VERBOSE=1 %{?_smp_mflags}

%install

%changelog
