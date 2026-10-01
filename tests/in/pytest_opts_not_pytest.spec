Name:           test
Version:        1.0
Release:        0
Summary:        test
License:        MIT
Group:          test

%description
test

%check
%python_expand pytest_opts+=" --ignore foo"
%pytest --pyargs bar $pytest_opts

%changelog
