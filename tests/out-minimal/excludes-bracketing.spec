%bcond_with[^\s]*
%add_maven_depmap
%attr(\s*\([^)]*\))?

%build
%cabal_test

%changelog
%check
%cmake
%cmake_[^\s]*
%config(\s*\([^)]*\))?
%configure
%create_exclude_filelist
%ctest
%defattr(\s*\([^)]*\))?
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
%files_fontsconf_file
%fillup_[^\s]*
%find_gconf_schemas
%find_lang
%gem_install
%gem_packages
%ghc_bin_build
%ghc_bin_install
%ghc_check_bootstrap
%ghc_fix_dynamic_rpath
%ghc_fix_rpath
%ghc_lib_build
%ghc_lib_install
%ghc_pkg_recache
%ghost
%glib2_gsettings_schema_[^\s]*

%global
%gpg_verify
%icon_theme_cache_post[^\s]*
%if(\s*\(.*)?
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
%kde_post_install
%kde4_makeinstall
%kernel_module_package
%kf5_makeinstall
%lang_package
%lang(\s*\([^)]*\))
%make_build
%make_install
%make_jobs
%makeinstall
%mime_database_post[^\s]*
%nagios_command_user_group_add
%nagios_user_group_add
%__os_install_post

%package
%patch[0-9]*
%perl_gen_filelist
%perl_make_install
%perl_process_[^\s]*
%pom_add_dep
%pom_remove_dep

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
%qmake5_install
%reconfigure_fonts_[^\s]*
%requires_[^\s]*
%restart_on_update
%run_permissions
%service_add_pre foo.service
%service_add_post foo.service
%service_del_preun foo.service
%service_del_postun foo.service
%set_permissions
%setup
%stop_on_removal
%suse_kernel_module_package
%suse_update_desktop_file
%systemd_preun
%systemd_requires
%tmpfiles_create
%triggerin
%triggerpostun
%triggerun
%udev_rules_update
%undefine
%verify[^\s]*
%verify(\s*\([^)]*\))?
%with
%without
%yast_build
%yast_install

%changelog
