%bcond_with betatest
Name:           patterns-cockpit
Version:        16.0
Release:        0
Summary:        Pattern for Cockpit, a web based remote system management interface
License:        MIT
URL:            http://en.opensuse.org/Patterns
Source0:        %{name}.rpmlintrc
Provides:       pattern() = cockpit
Provides:       pattern-icon() = pattern-generic
Provides:       pattern-order() = 9060
Provides:       pattern-visible()
BuildRequires:  patterns-rpm-macros
Obsoletes:      patterns-microos-cockpit
Provides:       patterns-microos-cockpit
ExclusiveArch:  x86_64 %{arm32} aarch64 ppc64le s390x riscv64
Requires:       cockpit
%pattern_advsysmgmt

%description
Packages required to run the Cockpit system management service.

%changelog
