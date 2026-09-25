Name:           foo
Version:        1.0
Release:        0
Summary:        Foo
License:        MIT
BuildRequires:  gcc
# test dependencies
# SECTION test requirements
# /SECTION
# nothing here yet
  %if 0%{?suse_version} > 1500
  %endif
# optional feature
%{?with_foo:
}

%description
Foo.

%changelog
