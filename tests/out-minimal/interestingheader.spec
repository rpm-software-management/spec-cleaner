#  Copyright (c) 2011 Edgar Aichinger <edogawa@aon.at>
#
# norootforbuild

Name:           din
Version:        5.2.1
Release:        0
Summary:        .spec file cleaner
Summary(de):    Ein Synthesizer der dritten Art
License:        GPL-2.0-or-later
Group:          Productivity/Multimedia/Sound/Midi
URL:            http://www.dinisnoise.org/
Source:         %{name}-%{version}.tar.bz2
Source1:        %{name}.png
BuildRequires:  Mesa
BuildRequires:  autoconf
BuildRequires:  gcc-c++
BuildRequires:  libircclient-devel
BuildRequires:  pkgconfig
BuildRequires:  update-desktop-files
BuildRequires:  pkgconfig(fftw3)
BuildRequires:  pkgconfig(fftw3f)
BuildRequires:  pkgconfig(fftw3l)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(liblo)
BuildRequires:  pkgconfig(sdl)
BuildRequires:  pkgconfig(tcl) >= 8.5
Requires:       Mesa
Requires:       fftw3
Requires:       jack
Requires:       tcl >= 8.5

%changelog
