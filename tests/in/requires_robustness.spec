#
# spec file for package requires_robustness
#
# Copyright (c) 2026 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). In either case, the license
# applied to this file or the package documents its terms.
#
# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


Name:           requires_robustness
Version:        1.0
Release:        0
Summary:        Test robustness of dependency parsing
License:        BSD-3-Clause
Group:          Development/Tools/Other
Provides:       kchmviewer = 8.0^fork
BuildRequires:  %?suse_sgx_gcc_major
Supplements:    modalias(mdio:0000000000110011100111??????????)
Requires:       (ibus or fcitx) %dnl boo#1251853
BuildRequires:  %{python_module mock} ## <-- not available anymore!
Requires:       foo # a normal comment
Supplements:    packageand(apache2:%name)
# API for Disabled Modules (ProductControl)
Requires:       yast2 >= 2.16.36
# After API cleanup
Requires:       yast2
# Reversed order: plain requirement first
Requires:       yast3
# Versioned requirement second
Requires:       yast3 >= 1.0

%description
Test robustness of dependency parsing.

%files

%changelog
