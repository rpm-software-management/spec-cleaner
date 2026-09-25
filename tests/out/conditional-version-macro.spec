BuildRequires:  gcc-c++
BuildRequires:  libxml2-devel %{?xml_min:>= %{xml_min}}
Requires:       openssl %{?el6: >= 1.0.1}
Requires:       python3
Requires:       python3-bar %{?bar_min:>= %{bar_min}}
Requires(post): selinux-policy %{!?_selinux_policy_version:= 1}

%changelog
