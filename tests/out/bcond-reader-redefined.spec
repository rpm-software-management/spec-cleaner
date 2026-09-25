%bcond_without docs
%global build_docs %{with docs}
%if 0%{?rhel}
%global build_docs 0
%endif
%if 0%{?suse_version}
%bcond_without tests
%global run_tests %{with tests}
%ifarch s390x
%global run_tests 0
%endif
%endif
Name:           bcond-reader-redefined
Version:        1.0
Release:        0
Summary:        Test overrides of bcond readers stay below them
License:        MIT
URL:            https://example.org/

%description
Test.

%build
echo %{build_docs} %{?run_tests}

%changelog
