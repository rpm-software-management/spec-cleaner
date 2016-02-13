#
# spec file for package conditionmultiline
#
# Copyright (c) 2013 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


BuildRequires:  something

%build
 bash ../configure \
 %ifnarch %{jit_arches}
     --with-jvm-variants=zero \
 %endif
     --with-libpng=system \
     --with-lcms=system \
     --with-stdc++lib=dynamic \
 %ifnarch %{arm}
     --with-num-cores="$NUM_PROC" \
 %endif
 make -j1

%ifarch %{jit_arches}
%if 0%{?suse_version} >= 1120
    --enable-nio2 \
%endif
%if %{with_systemtap}
    --enable-systemtap \
%endif
    --with-abs-install-dir=%{_jvmdir}/%{sdkdir} \
%endif
%if 0%{?suse_version} >= 1120
%if %{with bootstrap}
    --disable-pulse-java \
%else
    --enable-pulse-java \
%endif
    --enable-nss \
%endif
%if %{with bootstrap}
    --enable-bootstrap \
    --enable-bootstrap-tools \
    --with-javac=${JAVAC} \
    --with-ecj=%{_bindir}/ecj \
    --with-ecj-jar=${ECJJAR} \
    --with-jdk-home=%{_jvmdir}/java-1.5.0-gcj \
%else
    --disable-bootstrap \
%endif
%if %{with docs}
    --enable-docs \
%else
    --disable-docs \
%endif
    --with-xerces2-jar=%{_javadir}/xerces-j2-bootstrap.jar \
    --with-openjdk-src-zip=%{SOURCE1} \
%ifnarch %{arm} %{aarch64}
    --with-parallel-jobs=${NUMCPUS} \
%else
    --with-parallel-jobs=1 \
%endif
    --with-pkgversion=suse-%{release}-%{_arch}

%changelog
