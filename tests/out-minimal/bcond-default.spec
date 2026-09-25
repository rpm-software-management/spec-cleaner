%bcond tests 1
%bcond docs 0
%if %{with tests}
%global testsuite full
BuildRequires:  python3-pytest
%endif
Name:           bcond-default
Version:        1.0
Release:        0
Summary:        Test %%bcond with a default value
License:        MIT
URL:            https://example.org/

%description
Test.

%changelog
