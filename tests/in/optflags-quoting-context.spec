%build
cat > config.mk <<EOF
CFLAGS = $RPM_OPT_FLAGS -fPIC
EOF
echo 'CFLAGS=$RPM_OPT_FLAGS -fPIC' >> config.mk
sed -i 's|^CFLAGS = .*|CFLAGS = $RPM_OPT_FLAGS -fPIC|' Makefile
echo "it's" CFLAGS=$RPM_OPT_FLAGS ./build.sh
CXXFLAGS+=$RPM_OPT_FLAGS ./build.sh
CFLAGS=$RPM_OPT_FLAGS; export CFLAGS
FOO="a \"b"; BAR=$RPM_OPT_FLAGS ./build.sh
