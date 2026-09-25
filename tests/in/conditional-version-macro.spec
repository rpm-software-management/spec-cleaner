Requires:       python3-bar %{?bar_min:>= %{bar_min}}
Requires:       openssl %{?el6: >= 1.0.1}, python3
Requires(post): selinux-policy %{!?_selinux_policy_version:= 1}
BuildRequires:  libxml2-devel %{?xml_min:>= %{xml_min}} gcc-c++
