%define version %(rpm -q --qf '%{VERSION}' kernel-source)
%{?requires_ge:%requires_ge libapr1}
%requires_eq vlc
Requires:       mozilla-nspr >= %(rpm -q --queryformat '%{VERSION}' mozilla-nspr)
Requires:       mozilla-nss >= %(rpm -q --queryformat '%{VERSION}' mozilla-nss)
Requires:       mozilla-nspr-devel >= %(rpm -q --queryformat '%{VERSION}' mozilla-nspr-devel)
Requires:       mozilla-nss-devel >= %(rpm -q --queryformat '%{VERSION}' mozilla-nss-devel)
Requires:       ant = %(echo `rpm -q --queryformat '%{VERSION}' ant`)
Requires:       akonadi-runtime >= %( echo `rpm -q --queryformat '%{VERSION}' akonadi-runtime`)
Requires:       %(rpm --qf "%%{name}" -qf $(readlink -f %{_libdir}/libavcodec.so))(unrestricted)
Provides: NetworkManager-lang = %(rpm -q --queryformat '%{VERSION}' NetworkManager-lang)
