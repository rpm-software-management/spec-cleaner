#
# spec file for package interestingheader
#
# Copyright (c) 2013 SUSE LINUX GmbH, Nuernberg, Germany.
# Copyright (c) 2011 Edgar Aichinger <edogawa@aon.at>
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


BuildRequires:  gcc-c++
BuildRequires:  fftw3-devel
BuildRequires:  Mesa
BuildRequires:  libircclient-devel
BuildRequires:  liblo-devel
BuildRequires:  libjack-devel
BuildRequires:  tcl-devel >= 8.5
BuildRequires:  libSDL-devel
BuildRequires:  autoconf
BuildRequires:  update-desktop-files

Summary:        .spec file cleaner
Summary(de):    Ein Synthesizer der dritten Art
Name:           din
Version:        5.2.1
Release:        0.1
Source:         %{name}-%{version}.tar.bz2
Source1:        %{name}.png
Group:          Productivity/Multimedia/Sound/Midi
License:        GPL-2.0+
URL:            http://www.dinisnoise.org/
Vendor:         %{vendor}

Requires:       fftw3
Requires:       Mesa
Requires:       jack
Requires:       tcl >= 8.5

