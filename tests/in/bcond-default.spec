%bcond tests 1
%bcond docs 0
Name:           bcond-default
Version:        1.0
Release:        0
Summary:        Test %%bcond with a default value
License:        MIT
URL:            https://example.org/
%if %{with tests}
%global testsuite full
BuildRequires:  python3-pytest
%endif

%description
Test.

%changelog
