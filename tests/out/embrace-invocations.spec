%global _pyver %{lua: \
  local ver = string.sub(rpm.expand("%python"), string.len("python") + 1, -1); \
    print(string.format("%s.%s", string.sub(ver, 1, 1), string.sub(ver, 2, -1))); \
}
Name:           embrace-invocations
Version:        1.0
Release:        0
Summary:        Test %{name} package
License:        MIT
URL:            https://example.org/
Provides:       %name(xfrm6_raw) = %{version}-%{release}
Provides:       %plainpython(abi) = %{version}
%lang_package(foo)

%description
Test.

%files

%changelog
