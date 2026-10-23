Name:           macroforms
Version:        1.0
Release:        0
Summary:        Macro form spellings
License:        MIT
Source0:        %{name}-%{version}.tar.xz
Source1:        extra1.txt
Source2:        extra2.txt
Patch0:         fix0.patch
Patch1:         fix1.patch

%description
Macro form spellings stay as written in the minimal run.

%prep
%setup -q
# comment mentioning %{S:1} and %{P:1}
cp %{SOURCE0} %{PATCH0} .
cp %{SOURCE1} %{SOURCE2} %{PATCH1} .
tar xf prefix-%{SOURCE1}.tar.xz
echo %{?with_extra:%{SOURCE2}}
cp %{SOURCE1} .
cp %{SOURCE2} .
echo %{S:foo}

%install
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/%{name}/

%files
%{_datadir}/%{name}/

%changelog
