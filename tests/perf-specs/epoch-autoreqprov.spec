%global evr %{epoch}:%{version}-%{release}
Name:           epoch-autoreqprov
Version:        1.0
Summary:        Test
License:        MIT
Epoch:          2
Release:        0
AutoReqProv:    no

%description
Test.

%package devel
Summary:        Devel files
AutoReqProv:    on
Requires:       %{name} = %{evr}

%description devel
Devel files.

%package tools
Summary:        Tools
AutoReqProv:    off
Requires:       %{name} = %{epoch}:%{version}

%description tools
Tools.

%files

%files devel

%files tools

%changelog
