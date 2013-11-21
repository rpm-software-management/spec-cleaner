%package -n %libname
# remove the old non-versioned package (built in the bs for instance)
Provides:       libwpd = %version
Obsoletes:      libwpd < %version
Provides:       sysvinit:/sbin/init
Summary:        Library for Importing WordPerfect (tm) Documents
Group:          System/Libraries
