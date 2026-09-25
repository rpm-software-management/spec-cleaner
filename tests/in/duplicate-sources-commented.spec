Name:           duplicate-sources-commented
Version:        1.0
Release:        0
Summary:        Merge commented duplicated sources without losing other sources
License:        MIT
# main tarball
Source:         %{name}-%{version}.tar.gz
Source1:        extra.tar.gz
# listed twice by mistake
Source:         %{name}-%{version}.tar.gz

%description
Duplicated sources with a comment on each copy are merged into one line, keeping both comments.

%changelog
