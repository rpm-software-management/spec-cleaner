Name:           version-number-zeros
Version:        1.00%{?snapshot}
Release:        0
Summary:        Test
License:        MIT

%description
Test.

%build
%if %{suse_version} > 1500
./configure --with-limit=100%{?limit_suffix}
%endif

%changelog
