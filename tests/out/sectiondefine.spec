%build
# This is for build debugging purposed
export OIIOINC=`echo $PWD`
%define pwd $OIIOINC
%define oiioinclude %{pwd}/src/include
echo %{pwd}
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
mkdir -p build
cd build
# FIXME: you should use the %%cmake macros
cmake \
%ifarch ppc ppc64
    -DNOTHREADS=ON \
%endif
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DLIB_INSTALL_DIR=%{_libdir} \
    -DPYLIB_INSTALL_DIR=%{python_sitearch} \
    -DINSTALL_DOCS:BOOL=ON \
    -DDOC_INSTALL_DIR=%{_docdir}/%{name} \
    -DINSTALL_FONTS:BOOL=ON \
    -DBUILDSTATIC:BOOL=OFF \
    -DLINKSTATIC:BOOL=OFF \
    -DUSE_EXTERNAL_PUGIXML:BOOL=ON \
    -DUSE_FFMPEG:BOOL=OFF \
    -DUSE_OPENSSL:BOOL=ON \
    -DCMAKE_SKIP_RPATH:BOOL=ON \
    ..

%install
%global optflags    %{optflags} -D_REENTRANT -pipe -fPIE
export LDFLAGS="-Wl,-z,relro,-z,now -pie"
%configure \
%if ! %{with static_libs}
        --disable-static \
%endif
        --with-pic \
        --docdir=%{_docdir}/%{name}

%changelog
