Name:           buildroot
Version:        1.0
Release:        0
Summary:        BuildRoot handling
License:        MIT
BuildRequires:  compiler
# retained for the legacy build root
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
BuildRoot handling.

%package sub
Summary:        BuildRoot handling subpackage
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch

%description sub
BuildRoot handling subpackage.

%package legacy
Summary:        BuildRoot handling legacy subpackage
BuildRoot:      %_tmppath/%name-%version-build
BuildArch:      noarch

%description legacy
BuildRoot handling legacy subpackage.

%files
%files sub
%files legacy

%changelog
