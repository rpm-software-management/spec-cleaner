Name:           conditionaldeps
Version:        1.0
Release:        0
Summary:        Conditional dependency handling
License:        MIT
Group:          Development/Tools/Other

%define _with_ffmpeg 1

BuildRequires:  zeta-devel
%{?_with_faad2:BuildRequires:  pkgconfig(faad2)}
BuildRequires:  alpha-devel
# ffmpeg support is conditional
%{?_with_ffmpeg:
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libavcodec) >= 57.48.101
}
%if 0%{?suse_version} > 1500
BuildRequires:  suse-only-devel
%endif
Requires:       base-package

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
