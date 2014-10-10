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
