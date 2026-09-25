Name:           dupversionedfirst
Version:        1.0
Release:        0
Summary:        Versioned duplicate first
License:        MIT
URL:            https://example.org
# versioned first
BuildRequires:  foo >= 1.0
# unversioned second
BuildRequires:  foo
BuildRequires:  pkgconfig(libxml-2.0) >= 2.9
BuildRequires:  libxml2-devel
Requires:       bar > 2
Requires:       bar
Requires:       bar < 5
Requires:       baz >= 1
# commented unversioned duplicate
Requires:       baz
Provides:       prov = 1
Provides:       prov
Obsoletes:      obs < 2
Obsoletes:      obs

%description
Test.

%changelog
