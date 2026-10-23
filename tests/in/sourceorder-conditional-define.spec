Name:           sourceorder-conditional-define
Version:        2.0
Release:        0
Summary:        Conditional define block stays below the tags in minimal mode
License:        MIT
%if 0%{?suse_version} > 1500
%global flavour stable
%else
%global flavour legacy
%endif
#!BuildIgnore:  sourceorder-conditional-define-old
#!BuildIgnore:  sourceorder-conditional-define-older
BuildRequires:  zzz-pkg
BuildRequires:  aaa-pkg
Requires:       flavour-%{flavour}

%description
The conditional block defining the flavour macro is written below the
name and version tags it is grouped with; it stays there, as do the
pragma lines and the unsorted BuildRequires lines that follow it.

%files
%{_bindir}/sourceorder-conditional-define

%changelog
