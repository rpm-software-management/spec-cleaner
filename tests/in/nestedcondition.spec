%build
%if %{with meson}
%meson \
    --default-library=both \
    -Dselinux=true \
    -Dman=true \
    -Dgtk_doc=true \
    -Dfam=true \
%if %{with systemtap}
    -Dsystemtap=true \
%endif
    -Ddtrace=true \
    -Dinternal_pcre=false
%meson_build

%check
%meson_test
%else
autoreconf -fi
%configure \
    --enable-static \
    --enable-selinux \
    --enable-gtk-doc \
    --enable-man \
    --with-python=%{_bindir}/python3 \
%if %{with systemtap}
    --enable-systemtap \
%endif
    --with-pcre=system
%make_build
%endif
