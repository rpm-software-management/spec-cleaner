%install
rm -rf %{buildroot}
cp -a platform %{buildroot}
cp -a xterm $RPM_BUILD_ROOT
cp -r data/platform %{buildroot}
./install.sh --platform linux --prefix %{buildroot}
test -d %{buildroot} && rm -rf %{buildroot}
