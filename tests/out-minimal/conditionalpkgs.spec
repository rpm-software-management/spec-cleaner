%description
Apache 2, the successor to Apache 1.

Apache is the most used Web server software worldwide.

Some new features in Apache 2: - hybrid multiprocess, multithreaded
   mode for improved scalability

- multiprotocol support

- stream filtering

- IPv6 support

- new module API

New modules include: - mod_auth_db

- mod_auth_digest

- mod_charset_lite

- mod_dav

- mod_file_cache

Mod_ssl is no longer a separate package, but is now included in the
Apache distribution.

See %{_docdir}/apache2/, http://httpd.apache.org/, and
http://httpd.apache.org/docs-2.2/upgrading.html.

%if %worker
%package worker
Summary:        Apache 2 worker MPM (Multi-Processing Module)
Group:          Productivity/Networking/Web/Servers
Requires:       %{name} = %{version}
Provides:       %{pname}-MPM
%endif

%if %prefork
%package prefork
Summary:        Apache 2 "prefork" MPM (Multi-Processing Module)
Group:          Productivity/Networking/Web/Servers
Requires:       %{name} = %{version}
Provides:       %{pname}-MPM
%if 0%{?suse_version} >= 901 && 0%{?sles_version} != 9
Provides:       apache:%{_sbindir}/httpd
%endif
%endif

%if %event
%package event
Summary:        Apache 2 event MPM (Multi-Processing Module)
Group:          Productivity/Networking/Web/Servers
Requires:       %{name} = %{version}
Provides:       %{pname}-MPM
%endif

%if %itk
%package itk
Summary:        Apache 2 "ITK" MPM (Multi-Processing Module)
Group:          Productivity/Networking/Web/Servers
Requires:       %{name} = %{version}
Provides:       %{pname}-MPM
%endif

%changelog
