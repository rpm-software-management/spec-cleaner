%clean
rm -rf %{buildroot}

%{__brp} -e %{buildroot}
rm -f %{buildroot}/usr/share/doc

   # an indented comment is kept above the next section
%post
echo installed
