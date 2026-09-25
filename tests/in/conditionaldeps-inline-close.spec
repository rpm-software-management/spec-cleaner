Name:           conditionaldeps-inline-close
Version:        1.0
Release:        0
Summary:        Multi-line conditional blocks closed on their last line
License:        MIT
%{?snapshot:
Source0:        https://example.com/%{name}-%{snapshot}.tar.gz}
BuildRequires:  zeta-devel
%{?with_foo:
Requires:       zfoo
BuildRequires:  afoo-devel}
BuildRequires:  alpha-devel
%{?with_foo:
Requires:       ybar
%{?with_bar:
BuildRequires:  xbar-devel}}
Requires:       base-package

%description
Test conditional blocks closed at the end of a content line.

%changelog
