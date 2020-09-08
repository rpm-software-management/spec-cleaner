%check
%pyunittest
%pyunittest -v
%pyunittest tests -v
%pyunittest
%pyunittest -v -s tests
%pyunittest -v tests.test_cursors
%pyunittest openid.test.test_suite
%pyunittest_arch -v

%changelog
