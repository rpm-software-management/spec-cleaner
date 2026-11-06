%install
make install

# keep this note
%if 0%{?suse_version}
%files
%{_bindir}/foo
%endif

%changelog
