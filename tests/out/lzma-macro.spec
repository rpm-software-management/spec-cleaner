%prep
xz --format=lzma -dc %{SOURCE0} | tar -xf -
xz --format=lzma -dc %{SOURCE1} | tar -xf -

%files

%changelog
