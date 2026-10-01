Name:           python_expand_pytest_opts
Version:        1.0
Release:        0
Summary:        Test that pytest_opts shell var is not treated as pytest
License:        MIT
Group:          Development/Tools/Building

%description
Test that '%%python_expand pytest_opts+="..."' (shell variable assignment)
is not mistaken for a pytest invocation. The re_pytest regex must not
match 'pytest' inside 'pytest_opts'.

%prep

%build
%python_expand pytest_opts+=" --ignore foo"
%pytest --pyargs bar $pytest_opts

%install

%changelog
