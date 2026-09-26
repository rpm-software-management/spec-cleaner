# every distribution version macro spec-cleaner knows about, plus a doubled zero
Name:           buildservice-distros
Version:        1.0
Release:        0
Summary:        Test package
License:        MIT
URL:            https://example.org/buildservice-distros

%description
Test package.

%build
echo 0%{?centos_version}
echo 0%{?debian_version}
echo 0%{?fedora_version}
echo 0%{?mandriva_version}
echo 0%{?meego_version}
echo 0%{?rhel_version}
echo 0%{?sles_version}
echo 0%{?suse_version}
echo 0%{?ubuntu_version}
echo 0%{?suse_version}

%files

%changelog
