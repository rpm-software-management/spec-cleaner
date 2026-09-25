Name:           foo
Version:        1.0
Release:        0
Summary:        Foo
License:        MIT
URL:            https://example.com/foo
Source:         foo-%{version}.tar.gz
BuildSystem:    autotools

%description
Foo.

%prep -a
sed -i 's/foo/bar/' configure.ac

%conf -p
autoreconf -fiv

%build -p
%define _lto_cflags %{nil}
%if 0%{?suse_version} < 1600
export CC=gcc-13
%endif
export CFLAGS="%{optflags} -fno-strict-aliasing"

%install -a
%define mydocs %{_docdir}/foo
%if 0%{?suse_version}
rm -rf %{buildroot}%{mydocs}
%endif
install -D -m 644 README %{buildroot}%{mydocs}/README

%check -a
%global testargs --verbose
%if %{with tests}
./run-tests %{testargs}
%endif
echo done

%files
%{_bindir}/foo
%{_docdir}/foo

%changelog
