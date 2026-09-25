Name:           version-number-zeros
Version:        1.00%{?snapshot}
Release:        0
Summary:        Test
License:        MIT

%description
Test.

%build
%if 0%{?suse_version} > 1500
# FIXME: you should use the %%configure macro
./configure --with-limit=100%{?limit_suffix}
%endif

%changelog
