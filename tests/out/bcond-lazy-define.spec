%define use_bar %{with bar}
%define build_docs %{with docs}
%bcond_without bar
%bcond_without docs
%global bar_opts --bar=%{use_bar}
%if %{build_docs}
%define docdir doc
%endif
Name:           bcond-lazy-define
Version:        1.0
Release:        0
Summary:        Test globals reading a bcond through a lazy define stay below it
License:        MIT
URL:            https://example.org/

%description
Test.

%build
echo %{bar_opts} %{?docdir}

%changelog
