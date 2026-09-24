%define _with_ffmpeg 1
Name:           conditionaldeps
Version:        1.0
Release:        0
Summary:        Conditional dependency handling
License:        MIT
Group:          Development/Tools/Other
BuildRequires:  alpha-devel
BuildRequires:  zeta-devel
Requires:       base-package
%{?_with_faad2:BuildRequires:  pkgconfig(faad2)}
# ffmpeg support is conditional
%{?_with_ffmpeg:
BuildRequires:  pkgconfig(libavcodec) >= 57.48.101
BuildRequires:  pkgconfig(libavutil)
}
%if 0%{?suse_version} > 1500
BuildRequires:  suse-only-devel
%endif

%description
Test conditional dependencies.

%package utils
Summary:        Utilities
Group:          Development/Tools/Other
Requires:       other-package
%{?_with_sso:Requires: pkgconfig(sso-mib)}

%description utils
Utilities.

%changelog
