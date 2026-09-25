Name:           dupversionedfirst
Version:        1.0
Release:        0
Summary:        Versioned duplicate first
License:        MIT
URL:            https://example.org
# versioned first
# unversioned second
BuildRequires:  foo >= 1.0
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(libxml-2.0) >= 2.9
Requires:       bar < 5
Requires:       bar > 2
# commented unversioned duplicate
Requires:       baz >= 1
Provides:       prov = 1
Provides:       prov
Obsoletes:      obs < 2
Obsoletes:      obs

%description
Test.

%changelog
