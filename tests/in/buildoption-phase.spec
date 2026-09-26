# the plain BuildOption tag next to the phased ones, they are separate categories
Name:           buildoption-phase
Version:        1.0
Release:        0
Summary:        Test package
License:        MIT
URL:            https://example.org/buildoption-phase
BuildOption(build): -j4
BuildOption:    -O2
BuildOption(post): -P %{_smp_mflags}

%description
Test package.

%changelog
