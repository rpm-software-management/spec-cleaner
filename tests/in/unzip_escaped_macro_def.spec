Name:           unzip_escaped_macro_def
Version:        1.0
Release:        0
Summary:        Test that %%{__unzip} in macro def is not expanded
License:        MIT
Group:          Development/Tools/Building

%description
Test that '%%%%{__unzip}' (escaped) inside a macro definition is left
alone and not expanded to '%%unzip'. The %% escaping indicates a literal
percent in the macro body, not a macro to expand.

%define my_install() \
   extdir="%%{buildroot}" \
   %%{__unzip} -q -d "$extdir" "%%1" \
   %%{nil}

%prep

%build
%my_install foo.zip

%install

%changelog
