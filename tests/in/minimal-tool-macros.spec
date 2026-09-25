%install
%__make install DESTDIR=%{buildroot}
%__arch_install_post
%__python3 setup.py install

%changelog
