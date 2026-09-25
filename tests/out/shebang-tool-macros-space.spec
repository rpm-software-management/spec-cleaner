%prep
sed -i "1s|^#!.*|#! %{__python3}|" bin/foo
sed -i -e '1s|^#!.*perl|#! %{__perl}|' tools/bar.pl
sed -i '1s|^#!.*|#! %__python3|' bin/baz

%changelog
