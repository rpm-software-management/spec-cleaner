Name:           url_http_sudo
Summary:        Replace http with https if possible
License:        GPL-2.0-only
URL:            http://sudo.ws

%package google-http
Summary:        Http google.com
URL:            http://google.com

%package google-https
Summary:        Https google.com
URL:            https://google.com

%package with www
Summary:        www.google.com
URL:            www.google.com

%package without www
Summary:        google.com
URL:            google.com

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

%changelog
