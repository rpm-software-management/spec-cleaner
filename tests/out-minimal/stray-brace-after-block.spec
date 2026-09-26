# a %{?cond: block followed by a line that ends in }, the depth must be back to zero
%{?with_a:
%global x 1
}
Name:           stray-brace-after-block
Version:        1.0
Release:        0
Summary:        Test package
License:        MIT
URL:            https://example.org/stray-brace-after-block
BuildRequires:  foo}

%description
Test package.

%changelog
