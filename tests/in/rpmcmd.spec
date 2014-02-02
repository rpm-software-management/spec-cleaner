%define version %(rpm -q --qf '%{VERSION}' kernel-source)
%requires_eq vlc
Requires:       mozilla-nspr >= %(rpm -q --queryformat '%{VERSION}' mozilla-nspr)
Requires:       mozilla-nss >= %(rpm -q --queryformat '%{VERSION}' mozilla-nss)
Requires:       mozilla-nspr-devel >= %(rpm -q --queryformat '%{VERSION}' mozilla-nspr-devel)
Requires:       mozilla-nss-devel >= %(rpm -q --queryformat '%{VERSION}' mozilla-nss-devel)
Requires:       ant = %(echo `rpm -q --queryformat '%{VERSION}' ant`)
Requires:       akonadi-runtime >= %( echo `rpm -q --queryformat '%{VERSION}' akonadi-runtime`)
