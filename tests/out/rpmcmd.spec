%define version %(rpm -q --qf '%{VERSION}' kernel-source)
# FIXME: Use %requires_eq macro instead
Requires:       akonadi-runtime >= %( echo `rpm -q --queryformat '%{VERSION}' akonadi-runtime`)
# FIXME: Use %requires_eq macro instead
Requires:       ant = %(echo `rpm -q --queryformat '%{VERSION}' ant`)
# FIXME: Use %requires_eq macro instead
Requires:       mozilla-nspr >= %(rpm -q --queryformat '%{VERSION}' mozilla-nspr)
# FIXME: Use %requires_eq macro instead
Requires:       mozilla-nspr-devel >= %(rpm -q --queryformat '%{VERSION}' mozilla-nspr-devel)
# FIXME: Use %requires_eq macro instead
Requires:       mozilla-nss >= %(rpm -q --queryformat '%{VERSION}' mozilla-nss)
# FIXME: Use %requires_eq macro instead
Requires:       mozilla-nss-devel >= %(rpm -q --queryformat '%{VERSION}' mozilla-nss-devel)
%requires_eq    vlc

%changelog
