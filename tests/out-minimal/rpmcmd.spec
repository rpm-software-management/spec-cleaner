%define version %(rpm -q --qf '%{VERSION}' kernel-source)
Requires:       %(rpm --qf "%%{name}" -qf $(readlink -f %{_libdir}/libavcodec.so))(unrestricted)
Requires:       akonadi-runtime >= %( echo `rpm -q --queryformat '%{VERSION}' akonadi-runtime`)
Requires:       ant = %(echo `rpm -q --queryformat '%{VERSION}' ant`)
Requires:       mozilla-nspr >= %(rpm -q --queryformat '%{VERSION}' mozilla-nspr)
Requires:       mozilla-nspr-devel >= %(rpm -q --queryformat '%{VERSION}' mozilla-nspr-devel)
Requires:       mozilla-nss >= %(rpm -q --queryformat '%{VERSION}' mozilla-nss)
Requires:       mozilla-nss-devel >= %(rpm -q --queryformat '%{VERSION}' mozilla-nss-devel)
%requires_eq    vlc
%requires_ge    libapr1
Provides:       NetworkManager-lang = %(rpm -q --queryformat '%{VERSION}' NetworkManager-lang)

%changelog
