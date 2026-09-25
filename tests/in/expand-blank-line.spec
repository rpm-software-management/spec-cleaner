Name:           foo
Version:        1.0
Release:        0
%global _description %{expand:
Paragraph one about %{name}.

Paragraph two.}
%define foo_flags \
  --enable-bar \

BuildRequires:  gcc
Summary:        Foo
License:        MIT

%description %{_description}

%changelog
