%install
make install DESTDIR=%{buildroot}
%__arch_install_post
python3 setup.py install

%changelog
