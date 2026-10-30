Name:           unbrace-command-position
Version:        1.0
Release:        0
Summary:        Braced argument-taking macros in command position
License:        MIT
URL:            https://example.org/unbrace

%description
Braced argument-taking macros followed by options keep their braces.

%prep
%{cargo_prep}

%build
%{cargo_build} --locked -p foo
%cargo_build

%install
%{cargo_install} --no-default-features

%check
%{cargo_test} -p foo
%{?with_check:%{cargo_test} -p bar}

%files
%{_bindir}/foo

%changelog
