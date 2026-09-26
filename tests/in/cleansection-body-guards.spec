%clean
rm -rf %{buildroot}

%{__brp} -e %{buildroot}
rm -f %{buildroot}/usr/share/doc

   # an indented comment ends the clean section
%post
echo installed
