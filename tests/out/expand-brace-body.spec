Name:           foo
Version:        1.0
Release:        0
%global _description %{expand:
This is the tool %{name}
and it is nice.
See %{url}
%{?with_extra:It has extras.}
}
Summary:        Foo
License:        MIT
URL:            https://example.org
BuildRequires:  gcc

%description %{_description}

%changelog
