%check
%pyunittest
%pyunittest -v
%pyunittest discover tests -v
%pyunittest
%pyunittest discover -v -s tests
%pyunittest -v tests.test_cursors
%pyunittest openid.test.test_suite
%pyunittest_arch -v

%changelog
