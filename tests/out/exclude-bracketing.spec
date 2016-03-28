#
# spec file for package exclude-bracketing
#
# Copyright (c) 2013 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


%bcond_with[^\s]*
%aarch64
%add_maven_depmap
%arm
%attr

%build
%cmake
%cmake_[^\s]*
%configure
%config
%create_exclude_filelist
%defattr
%define
%defined

%description
%desktop_database_post[^\s]*
%dir
%doc
%docdir
%else
%endif
%exclude
%fdupes

%files
%defattr(-,root,root)
%fillup_[^\s]*
%find_lang
%gem_install
%gem_packages
%ghost

%global
%gpg_verify

%changelog
%check
%icon_theme_cache_post[^\s]*
%if
%ifarch
%ifnarch
%include
%insserv_[^\s]*

%install
%install_info
%install_info_delete
%jar
%java
%javac
%jpackage_script
%ix86
%kde4_makeinstall
%kde_post_install
%kf5_makeinstall
%{lang}
%lang_package
%{make_build}
%make_jobs
%make_install
%mime_database_post[^\s]*

%package
%patch[0-9]*
%perl_gen_filelist
%perl_make_install
%perl_process_[^\s]*

%post
%posttrans
%postun
%pre

%prep
%pretrans
%preun
%py_compile
%qmake
%qmake5
%requires_[^\s]*
%restart_on_update
%run_permissions
%service_(add|del)}_[^\s]*
%setup
%set_permissions
%stop_on_removal
%suse_kernel_module_package
%suse_update_desktop_file
%systemd_requires
%triggerin
%triggerpostun
%triggerun
%undefine
%verify[^\s]*
%yast_(build|install)}[^\s]*

%changelog
