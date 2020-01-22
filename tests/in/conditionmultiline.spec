BuildRequires: something

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
%elifarch %{ix86}
    --with-parallel-jobs=2 \
%else
    --with-parallel-jobs=1 \
%endif
    --with-pkgversion=suse-%{release}-%{_arch}
