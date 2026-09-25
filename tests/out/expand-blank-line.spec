%define foo_flags \
  --enable-bar \

Name:           foo
Version:        1.0
Release:        0
%global _description %{expand:
Paragraph one about %{name}.

Paragraph two.}
Summary:        Foo
License:        MIT
BuildRequires:  gcc

%description %{_description}

%changelog
