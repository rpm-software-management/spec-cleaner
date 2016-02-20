#
# spec file for package langpackage
#
# Copyright (c) 2013 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


%package -n something-lang
# FIXME: consider using %%lang_package macro
Summary:        Something
# FIXME: use correct group, see "https://en.opensuse.org/openSUSE:Package_group_guidelines"
Group:          Whatever

%package lang
# FIXME: consider using %%lang_package macro
Summary:        Something
# FIXME: use correct group, see "https://en.opensuse.org/openSUSE:Package_group_guidelines"
Group:          Whatever

%package lang
# I have reason not to convert this to lang macro
Summary:        Something
# FIXME: use correct group, see "https://en.opensuse.org/openSUSE:Package_group_guidelines"
Group:          Whatever

%package -n %{_name}
Summary:        Evolution Plugin for RSS Feeds Support
Group:          Productivity/Networking/Email/Clients
Recommends:     %{_name}-lang
Provides:       %{name} = %{version}

%changelog
