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
%ctest
%defattr(\s*\([^)]*\))?
%define
%defined

%description
%desktop_database_post[^\s]*
%dir
%doc
%docdir
%electron_check_native
%electron_rebuild
%else
%endif
%exclude
%fdupes

%files
%files_fontsconf_file
%fillup_[^\s]*
%find_lang
%gem_install
%gem_packages
%ghc_bin_build
%ghc_bin_install
%ghc_fix_rpath
%ghc_lib_build
%ghc_lib_install
%ghc_pkg_recache
%ghost
%glib2_gsettings_schema_[^\s]*
%gpg_verify
%icon_theme_cache_post[^\s]*
%if something
%ifarch
%ifnarch
%include
%insserv_[^\s]*

%install
%install_info
%install_info_delete
%jpackage_script
%kernel_module_package
%kf5_makeinstall
%kf6_build
%kf6_install
%lang_package
%lang(\s*\([^)]*\))
%make_build
%make_install
%make_jobs
%make_install
%mime_database_post[^\s]*
%nagios_command_user_group_add
%nagios_user_group_add
%__os_install_post
%ocaml_create_file_list
%ocaml_dune_build
%ocaml_dune_install
%ocaml_dune_setup
%ocaml_dune_test
%octave
%octave_pkg_src
%octave_pkg_test

%package
%patch[0-9]*
%perl_gen_filelist
%perl_make_install
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
%pyqt_install
%python_alternative
%python_install_alternative
%python_uninstall_alternative
%python2_only
%python3_only
%pypy3_only
%pycache_only
%python3_build
%python2_install
%pypy3_install
%python_exec
%python_expand
%python_subpackages
%qmake
%qmake5
%qmake5_install
%qmake6
%qmake6_build
%qmake6_install
%qt6_build
%qt6_install
%reconfigure_fonts_[^\s]*
%regenerate_initrd_post
%regenerate_initrd_posttrans
%requires_[^\s]*
%restart_on_update
%run_permissions
%service_add_pre foo.service
%service_add_post foo.service
%service_del_preun foo.service
%service_del_postun foo.service
%set_build_flags
%set_permissions
%setup
%setup_openmpi
%stop_on_removal
%suse_kernel_module_package
%suse_update_desktop_file
%suseconfig_fonts_prereq
%systemd_preset_post
%systemd_preset_posttrans
%systemd_preset_pre
%systemd_preun
%systemd_requires
%systemd_user_preset_post
%systemd_user_preset_posttrans
%systemd_user_preset_pre
%tmpfiles_create

%triggerin

%triggerpostun

%triggerun
%udev_rules_update
%undefine
%update_bootloader_posttrans
%verify[^\s]*
%verify(\s*\([^)]*\))?
%with
%without
%yast_build
%yast_install

%changelog
