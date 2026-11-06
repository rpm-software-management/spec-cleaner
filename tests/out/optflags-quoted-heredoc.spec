%build
echo '$RPM_OPT_FLAGS'
cat > script.sh <<'EOF'
CFLAGS=$RPM_OPT_FLAGS
EOF
cat > config.mk <<EOF
CFLAGS = %{optflags} -fPIC
EOF

%changelog
