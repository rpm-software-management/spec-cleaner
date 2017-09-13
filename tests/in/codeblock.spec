Name:           codeblock
# MANUAL
BuildRequires:  aaa
BuildRequires:  bbb
# /MANUAL
# SECTION the testing dependencies
BuildRequires:  python-nose
BuildRequires:  python-mock
# /SECTION
### COMMON-PATCH-BEGIN ###
# implement "--record-rpm" option for distutils installations
Patch01:        Python-3.0b1-record-rpm.patch
# support lib-vs-lib64 distinction
Patch02:        Python-3.5.0-multilib.patch
# securing usage of readlink/realpath in PySys_SetArgv
Patch03:        python-2.6b1-canonicalize2.patch
# support finding packages in /usr/local, install to /usr/local by default
Patch04:        python-3.3.0b1-localpath.patch
# replace DATE, TIME and COMPILER by fixed definitions to aid reproducible
# builds
Patch06:        python-3.3.0b1-fix_date_time_compiler.patch
# fix wrong include path in curses-panel module
Patch15:        python-3.3.0b1-curses-panel.patch
# POSIX_FADV_WILLNEED throws EINVAL. Use a different constant in test
Patch09:        python-3.3.0b1-test-posix_fadvise.patch
# Disable global and distutils sysconfig comparison test, we deviate from the
# default depending on optflags
Patch12:        python-3.3.3-skip-distutils-test_sysconfig_module.patch
# Raise timeout value for test_subprocess
Patch07:        subprocess-raise-timeout.patch
# PATCH-FIX-UPSTREAM Fix argument passing in libffi for aarch64
Patch19:        python-2.7-libffi-aarch64.patch
# PATCH-FIX-UPSTREAM python3-ncurses-6.0-accessors.patch dimstar@opensuse.org
# -- Fix build with NCurses 6.0 and OPAQUE_WINDOW set to 1
Patch20:        python3-ncurses-6.0-accessors.patch
# PATCH-FIX-UPSTREAM Python-3.5.1-fix_lru_cache_copying.patch -- Fix copying
# the lru_cache() wrapper object -- https://bugs.python.org/issue25447
Patch30:        Python-3.5.1-fix_lru_cache_copying.patch
### COMMON-PATCH-END ###
BuildRequires:  test
# MANUAL BEGIN
BuildRequires:  pkgconfig(libxml-2.0) >= 2.9.0
Provides:       perl-XML-LibXML-Common = %{version}
Obsoletes:      perl-XML-LibXML-Common < %{version}
# MANUAL END
Patch05:        somepatch.patch
%build
### COMMON-CONFIG-BEGIN ###
export PATH=$PATH:/sbin:%{_prefix}/sbin
sed -ie "s/%{device_mapper_version}/1.03.01/g" VERSION_DM
%configure \
    --enable-dmeventd --enable-cmdlib \
    --enable-udev_rules --enable-udev_sync \
    --with-udev-prefix="%{_prefix}/" \
    --enable-selinux \
    --enable-pkgconfig \
    --with-usrlibdir=%{_libdir} \
    --with-usrsbindir=%{_sbindir} \
    --with-default-dm-run-dir=/run \
    --with-tmpfilesdir=%{_tmpfilesdir} \
    --with-thin=internal \
    --with-device-gid=6 \
    --with-device-mode=0640 \
    --with-device-uid=0 \
    --with-dmeventd-path=%{_sbindir}/dmeventd \
    --with-thin-check=%{_sbindir}/thin_check \
    --with-thin-dump=%{_sbindir}/thin_dump \
    --with-thin-repair=%{_sbindir}/thin_repair \
    $extra_opts
### COMMON-CONFIG-END ###

%changelog
