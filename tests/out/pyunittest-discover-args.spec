%check
%pyunittest -v
%pyunittest discover -s tests -t .
%pyunittest discover -p "test_*.py"
%pyunittest discover tests
%pyunittest discover -v -s test
%pyunittest_arch discover -s test -v
%pyunittest_arch

%changelog
