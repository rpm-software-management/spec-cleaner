%install
cp -a platform %{buildroot}
cp -a xterm %{buildroot}
cp -r data/platform %{buildroot}
./install.sh --platform linux --prefix %{buildroot}

%changelog
