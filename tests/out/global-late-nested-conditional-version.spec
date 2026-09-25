Name:           global-late-nested-conditional-version
Release:        0
%if 0%{?suse_version}
%if 0%{?suse_version} > 1500
Version:        2.0
%else
Version:        1.0
%endif
%global major %(echo %{version} | cut -d. -f1)
%else
%global major 3
Version:        3.0
%endif
Summary:        Test a nested global stays below a nested conditional Version
License:        MIT
URL:            https://example.org/
Provides:       major(%{major})

%description
Test.

%changelog
