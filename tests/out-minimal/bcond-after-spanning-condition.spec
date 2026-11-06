Name:           foo
Version:        1.0
Release:        0
Summary:        Foo
License:        MIT
URL:            https://example.com
Source0:        foo-1.0.tar.gz

%description
Foo.

%if %{with foo}
%build
make foo
%endif

%bcond_with bar
make bar

%changelog
