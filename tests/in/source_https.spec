%define         tarname    Python-%{version}
%define         folderversion %{version}
Name:           python311
Version:        3.11.8
Summary:        Replace http with https if possible
License:        GPL-2.0
Source0:        http://www.python.org/ftp/python/%{folderversion}/%{tarname}.tar.xz
Source1:        http://www.python.org/ftp/python/%{folderversion}/%{tarname}.tar.xz.asc
Source3:        http://google.com
Source4:        https://google.com
Source5:        www.google.com
Source6:        google.com
# non existent
Source7:        http://thishopefullydoesnexist.com
# Certificate
Source8:        http://expired.badssl.com/
Source9:        http://wrong.host.badssl.com/
Source10:       http://null.badssl.com/
# URL is FTP (issue#258)
Source11:       ftp://ftp.null.badssl.com/
Source12:       ftp.null.badssl.com/
# other prefix
Source13:       abc://null.badssl.com/
Source14:       http://xavprods.free.fr/lzx
