%define oname foo
%bcond_with docs
%if 0%{?with_docs}
%define docflag 1
%endif
%if 0%{!?with_docs:1}
%define nodocflag 1
%endif
%{!?with_py3:%global with_py3 1}
%if 0%{?with_py3}
%global pyver 3
%endif
Name:           bcond-question-with
Version:        1.0
Release:        0
Summary:        Test %%if 0%%{?with_x} conditions stay below the bcond
License:        MIT
URL:            https://example.org/

%description
Test.

%changelog
