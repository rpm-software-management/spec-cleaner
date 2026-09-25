%define _name glib
Name:           glib2
Version:        1.0
Release:        0
Summary:        Keep Recommends on a lang package the macro does not generate
License:        MIT
Recommends:     %{name}-lang

%description
The %%lang_package macro generates only %%{name}-lang here, so a Recommends
on another macro-named lang package is not redundant and must be kept.

%package -n gio-tool
Summary:        Tool
Recommends:     %{_name}-lang

%description -n gio-tool
Tool.

%lang_package

%changelog
