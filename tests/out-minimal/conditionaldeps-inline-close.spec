Name:           conditionaldeps-inline-close
Version:        1.0
Release:        0
Summary:        Multi-line conditional blocks closed on their last line
License:        MIT
BuildRequires:  alpha-devel
BuildRequires:  zeta-devel
Requires:       base-package
%{?snapshot:
Source0:        https://example.com/%{name}-%{snapshot}.tar.gz
}
%{?with_foo:
BuildRequires:  afoo-devel
Requires:       zfoo
}
%{?with_foo:
Requires:       ybar
%{?with_bar:
BuildRequires:  xbar-devel
}
}

%description
Test conditional blocks closed at the end of a content line.

%changelog
