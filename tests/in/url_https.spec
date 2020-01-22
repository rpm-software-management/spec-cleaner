Name:           url_http_sudo
Summary:        Replace http with https if possible
License:        GPL-2.0
Url:            http://sudo.ws

%package google-http
Summary: Http google.com
Url: http://google.com

%package google-https
Summary: Https google.com
Url: https://google.com

%package with www
Summary: www.google.com
Url: www.google.com

%package without www
Summary: google.com
Url: google.com

%package non-existing
Summary: This page doesn't exist
Url: http://thishopefullydoesnexist.com

# Certificate

%package expired
Summary: Expired certificate
Url: http://expired.badssl.com/

%package wronghost
Summary: Wrong host
Url: http://wrong.host.badssl.com/

%package null
Summary: Null cipher suite
Url: http://null.badssl.com/

# URL is FTP (issue#258)
%package ftp
Summary: Url is FTP
Url: ftp://ftp.null.badssl.com/

%package ftp1
Summary: Url is FTP
Url: ftp.null.badssl.com/

# other prefix
%package other
Summary: Url is not http, https or ftp
Url: abc://null.badssl.com/

%package brokenserver
Summary:        The server reconnects and cycles
URL:            http://xavprods.free.fr/lzx
