%package -n %libname
Summary:        Library for Importing WordPerfect (tm) Documents
Group:          System/Libraries
# remove the old non-versioned package (built in the bs for instance)
Provides:       libwpd = %version
Obsoletes:      libwpd < %version
Provides:       sysvinit:/sbin/init

%changelog
