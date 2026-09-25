%files
%{_bindir}/foo

%changelog
%if %{defined autochangelog}
%autochangelog
%else
* Mon Jan 01 2024 Jane Doe <jane@example.org> - 1.0-1
- Initial package
%endif
