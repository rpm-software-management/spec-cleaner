Name:           duplicate-sources
Version:        1.0
Release:        0
Summary:        Merge duplicated sources without losing other sources
License:        MIT
# listed twice by mistake
Source:         %{name}-%{version}.tar.gz
Source1:        extra.tar.gz

%description
Duplicated sources are merged into one line, keeping the comment.

%changelog
