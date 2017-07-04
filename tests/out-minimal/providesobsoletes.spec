%package -n %libname
Summary:        Library for Importing WordPerfect (tm) Documents
Group:          System/Libraries
Provides:       NetworkManager-lang = %(rpm -q --queryformat '%{VERSION}' NetworkManager-lang)
Obsoletes:      NetworkManager-lang < %(rpm -q --queryformat '%{VERSION}' NetworkManager-lang)
# remove the old non-versioned package (built in the bs for instance)
Provides:       libwpd = %version
Obsoletes:      libwpd < %version
Provides:       sysvinit:/sbin/init
# yes this is bogus and typo
Provides:       lib{name}-devel = %{version}
Obsoletes:      lib{name}-devel < %{version}
Provides:       sgpio:/{%{_bindir}}/ledctl
Provides:       vdirsyncer = %{version}

%changelog
