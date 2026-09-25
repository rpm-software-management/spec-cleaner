%bcond_without bar
%define use_bar %{with bar}
%global bar_opts --bar=%{use_bar}
%bcond_without docs
%define build_docs %{with docs}
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
