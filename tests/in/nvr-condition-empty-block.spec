Name:           nvr-condition-empty-block
%if 0%{?suse_version}
%if 0%{?sle_version}
Version:        1.0
%else
Version:        2.0
%endif
%if 0%{?is_opensuse}
%endif
%else
Version:        3.0
%endif
Release:        0
Summary:        Test an empty block after a conditional Version is dropped
License:        MIT
URL:            https://example.org/

%description
Test.

%changelog
