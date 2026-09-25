%prep
%{__lzma} -dc %{SOURCE0} | tar -xf -
%__lzma -dc %{SOURCE1} | tar -xf -

%files
