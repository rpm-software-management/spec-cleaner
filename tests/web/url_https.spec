Name:           url_http_sudo
Summary:        Replace http with https if possible
License:        GPL-2.0-only
URL:            https://sudo.ws

%package google-http
Summary:        Http google.com
URL:            https://google.com

%package google-https
Summary:        Https google.com
URL:            https://google.com

%package with www
Summary:        www.google.com
URL:            https://www.google.com

%package without www
Summary:        google.com
URL:            https://google.com

%package non-existing
Summary:        This page doesn't exist
URL:            http://thishopefullydoesnexist.com
# Certificate

%package expired
Summary:        Expired certificate
URL:            http://expired.badssl.com/

%package wronghost
Summary:        Wrong host
URL:            http://wrong.host.badssl.com/

%package null
Summary:        Null cipher suite
URL:            http://null.badssl.com/
# URL is FTP (issue#258)
%package ftp
Summary:        Url is FTP
URL:            ftp://ftp.null.badssl.com/

%package ftp1
Summary:        Url is FTP
URL:            ftp.null.badssl.com/
# other prefix
%package other
Summary:        Url is not http, https or ftp
URL:            abc://null.badssl.com/

%package brokenserver
Summary:        The server reconnects and cycles
URL:            http://xavprods.free.fr/lzx

%changelog
