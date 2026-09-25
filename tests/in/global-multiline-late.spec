%global tarver %{version}
%global desc \
Some long text \
continued here.
%define lazy \
%global notmoved %{version}
Name:           globalmultiline
Version:        1.0
Release:        0
%global short_version %(echo %{version} | cut -d. -f1-2)
%global _description %{expand:
Built from version %{version}.
}
%global longdesc \
Version %{version} text \
continued here.
Summary:        Multiline global order
License:        MIT
URL:            https://example.org
Source:         foo-%{tarver}.tar.gz

%description %{_description}

%changelog
