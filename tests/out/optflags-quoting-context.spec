%build
cat > config.mk <<EOF
CFLAGS = %{optflags} -fPIC
EOF
echo 'CFLAGS=%{optflags} -fPIC' >> config.mk
sed -i 's|^CFLAGS = .*|CFLAGS = %{optflags} -fPIC|' Makefile
echo "it's" CFLAGS="%{optflags}" ./build.sh
CXXFLAGS+="%{optflags}" ./build.sh
CFLAGS="%{optflags}"; export CFLAGS
FOO="a \"b"; BAR="%{optflags}" ./build.sh

%changelog
