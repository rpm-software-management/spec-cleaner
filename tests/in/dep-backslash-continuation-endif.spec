Name:           dep-backslash-continuation-endif
Version:        1.0
Release:        0
Summary:        Test
License:        MIT
%if %{with foo}
BuildRequires:  bar \
%endif
BuildRequires:  after

%description
Test.

%files

%changelog
