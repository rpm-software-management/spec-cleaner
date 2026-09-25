%define pkg_file() %1-%2.tar.gz
Name:           url-escapes
Version:        1.0
Release:        0
Summary:        Test that percent-encoded URLs are not curlified
License:        MIT
URL:            https://example.org/My%20Project
Source0:        https://gitlab.com/api/v4/projects/group%2Fproject/repository/archive.tar.gz
Source1:        https://example.org/My%20Project-%{version}.tar.gz
Source2:        https://example.org/KeePass%202.x/%{version}/KeePass-%{version}.zip
Source3:        https://example.org/Project%20%{version}/foo%28bar%29.tar.gz
Source4:        https://example.org/%7Euser/foo.tar.gz

%description
Test.

%prep
cp %{SOURCE1} My%20Project.tar.gz

%changelog
