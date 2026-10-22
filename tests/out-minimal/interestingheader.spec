#  Copyright (c) 2011 Edgar Aichinger <edogawa@aon.at>
#
# norootforbuild

BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(fftw3)
BuildRequires:  pkgconfig(fftw3f)
BuildRequires:  pkgconfig(fftw3l)
BuildRequires:  Mesa
BuildRequires:  libircclient-devel
BuildRequires:  pkgconfig(liblo)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(tcl) >= 8.5
BuildRequires:  libSDL-devel
BuildRequires:  autoconf
BuildRequires:  update-desktop-files
BuildRequires:  pkgconfig
Summary:        .spec file cleaner
Summary(de):    Ein Synthesizer der dritten Art
Name:           din
Version:        5.2.1
Release:        0
Source:         %{name}-%{version}.tar.bz2
Source1:        %{name}.png
Group:          Productivity/Multimedia/Sound/Midi
License:        GPL-2.0-or-later
URL:            http://www.dinisnoise.org/
Requires:       fftw3
Requires:       Mesa
Requires:       jack
Requires:       tcl >= 8.5

%changelog
