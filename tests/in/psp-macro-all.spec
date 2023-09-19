#
# spec file
#
# Copyright (c) 2023 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%{?sle15allpythons}
Name:           python-munch
Version:        3.0.0
Release:        0
BuildRequires:  python-rpm-macros
Requires:       python-six
BuildArch:      noarch
# SECTION test requirements
BuildRequires:  %{python_module pytest}
BuildRequires:  %{python_module six}

%changelog

