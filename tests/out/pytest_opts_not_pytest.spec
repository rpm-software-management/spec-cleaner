Name:           test
Version:        1.0
Release:        0
Summary:        test
License:        MIT
# FIXME: use correct group or remove it, see "https://en.opensuse.org/openSUSE:Package_group_guidelines"
Group:          test

%description
test

%check
%python_expand pytest_opts+=" --ignore foo"
%pytest --pyargs bar $pytest_opts
%python_exec -m unittest2 discover -v

%changelog
