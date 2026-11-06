Name:           langrecommendsstringmultidep
Version:        1.0
Release:        0
Summary:        Keep a string-kept Recommends holding more than the lang dep
License:        MIT
Recommends:     %{name}-lang
Recommends:     %{name}-lang %(rpm -q --queryformat '%{VERSION}' glibc)

%description
A Recommends line kept whole as one string (here, an rpm call) whose
first word is the own -lang dep must survive the lang pruning: dropping
the whole line would drop the other deps on it too.

%package -n %{name}-lang
Summary:        Translations for %{name}

%description -n %{name}-lang
Translations for %{name}.

%lang_package

%changelog
