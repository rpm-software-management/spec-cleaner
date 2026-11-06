Name:           dep-backslash-continuation-endif
Version:        1.0
Release:        0
Summary:        Test
License:        MIT
BuildRequires:  after
%if %{with foo}
BuildRequires:  bar
%endif

%description
Test.

%files

%changelog
