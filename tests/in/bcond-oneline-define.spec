%bcond_without docs
%{?with_docs:%define docflag 1}
Name:           bcond-oneline-define
Version:        1.0
Release:        0
Summary:        Test a one-line conditional define reading a bcond stays below it
License:        MIT
URL:            https://example.org/

%description
Test.

%build
echo %{?docflag}

%changelog
