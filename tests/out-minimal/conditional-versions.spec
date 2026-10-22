# rpm accepts these conditional version spellings, the dependency must stay one value
Name:           conditional-versions
Version:        1
Release:        0
Summary:        Test
License:        MIT
BuildRequires:  foo %{?bar:>= 1}
BuildRequires:  foo %{??bar:>= 1}
BuildRequires:  foo %{?!bar:>= 1}
BuildRequires:  foo %{!?bar:>= 1}
BuildRequires:  foo %{?bar:>=1}
Requires:       foo
Requires:       bar %{?baz:>= 1}

%description
Test.

%files

%changelog
