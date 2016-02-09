#
# spec file for package whitespace
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


%description
mpv is a movie player based on MPlayer and mplayer2. It supports a wide variety of video
file formats, audio and video codecs, and subtitle types.

%description
mpv is a movie player based on MPlayer and mplayer2. It supports a wide variety of video
file formats, audio and video codecs, and subtitle types.

%description
mpv is a movie player based on MPlayer and mplayer2. It supports a wide variety of video
file formats, audio and video codecs, and subtitle types.

%files
%defattr(-,root,root)
%doc LICENSE Copyright README.md etc/example.conf etc/encoding-example-profiles.conf etc/input.conf
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_datadir}/applications/%{name}.desktop

%{_datadir}/icons/hicolor/*/apps/%{name}.png

%changelog
