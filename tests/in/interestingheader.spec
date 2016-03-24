#  Copyright (c) 2011 Edgar Aichinger <edogawa@aon.at>
#
# norootforbuild

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
Vendor:         %vendor
Prefix:         /usr

Requires:       fftw3
Requires:       Mesa
Requires:       jack
Requires:       tcl >= 8.5
