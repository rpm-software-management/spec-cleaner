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
echo %{centos_version}
echo %{debian_version}
echo %{fedora_version}
echo %{mandriva_version}
echo %{meego_version}
echo %{rhel_version}
echo %{sles_version}
echo %{suse_version}
echo %{ubuntu_version}
echo 00%{?suse_version}

%files

%changelog
