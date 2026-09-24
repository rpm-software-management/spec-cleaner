Name:           langrecommendsrpmcall
Version:        1.0
Release:        0
Summary:        Keep rpm-call Recommends with %%lang_package
License:        MIT
Recommends:     %(rpm -q --queryformat '%{VERSION}' glibc)

%description
A Recommends evaluated from an rpm call is kept as an opaque string and
must survive the lang subpackage pruning.

%package -n %{name}-lang
Summary:        Translations for %{name}

%description -n %{name}-lang
Translations for %{name}.

%lang_package

%changelog
