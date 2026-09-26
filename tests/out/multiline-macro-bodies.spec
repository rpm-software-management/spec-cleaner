# A lua or shell macro body left open continues on the next lines
%define luafoo %{lua:
print("1")
}
%global shfoo %(echo 1 |
  tr 1 2)
%{?with_bar:
%define luabar %{lua:
print("3")
}
}
Name:           multiline-macro-bodies
Version:        1.0
Release:        0
Summary:        Test
License:        MIT
Provides:       foo = %{luafoo}
Provides:       bar = %{shfoo}

%description
Test.

%files

%changelog
