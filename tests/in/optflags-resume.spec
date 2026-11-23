%if %{with foo}
%build
export RPM_OPT_FLAGS="$(echo $RPM_OPT_FLAGS | sed -e 's/-Wall//g')"
%endif
CFLAGS="$RPM_OPT_FLAGS" ./configure

%if %{with foo}
%install
cat > x <<'EOF'
%endif
CFLAGS=$RPM_OPT_FLAGS
EOF
