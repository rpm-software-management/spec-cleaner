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
cp %{S:0} %{P:0} .
cp %{S:1} %{S:2} %{P:1} .
tar xf prefix-%{S:1}.tar.xz
echo %{?with_extra:%{S:2}}
cp %{SOURCE1} .
cp %SOURCE2 .
echo %{S:foo}

%install
install -m 644 %{S:1} %{buildroot}%{_datadir}/%{name}/

%files
%{_datadir}/%{name}/
