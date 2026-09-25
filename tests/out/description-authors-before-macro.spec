Name:           description-authors-before-macro
Version:        1.0
Release:        0
Summary:        Macros after a removed Authors block
License:        MIT

%description
Foo is a tool for testing.

%lang_package

%package extra
Summary:        Extra files

%description extra
Extra files for foo.

%if 0%{?suse_version} > 1500
%define with_extra 1
%endif

%prep
%setup -q

%build
%make_build

%install
%make_install
%find_lang %{name}

%files
%license COPYING

%files extra
%{_datadir}/foo

%files lang -f %{name}.lang

%changelog
