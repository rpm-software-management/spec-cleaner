%build
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -U_FORTIFY_SOURCE"
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-Wall//g' -e 's/-mbranch-protection=standard//g'`
CFLAGS="$RPM_OPT_FLAGS"
echo "CFLAGS=$CFLAGS"

%install
CFLAGS="$RPM_OPT_FLAGS"

%check
FOO=1; RPM_OPT_FLAGS="$RPM_OPT_FLAGS -x"
CFLAGS="$RPM_OPT_FLAGS"
