Name:           epoch-autoreqprov
Version:        1.0
Release:        0
Epoch:          2
%global evr %{epoch}:%{version}-%{release}
Summary:        Test
License:        MIT
AutoReqProv:    no

%description
Test.

%package devel
Summary:        Devel files
Requires:       %{name} = %{evr}

%description devel
Devel files.

%package tools
Summary:        Tools
Requires:       %{name} = %{epoch}:%{version}
AutoReqProv:    off

%description tools
Tools.

%files

%files devel

%files tools

%changelog
