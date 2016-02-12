#
# spec file for package bconds
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


%{!?aarch64:%global aarch64 aarch64 arm64 armv8}
%global jit_arches %ix86 x86_64 %aarch64 ppc64 ppc64le
%global test_arches %ix86 x86_64 ppc64 ppc64le
%global icedtea_version 2.5.1
%global icedtea_sound_version 1.0.1
%global mauvedate 2008-10-22
%global buildoutputdir openjdk.build/
# Convert an absolute path to a relative path.  Each symbolic link is
# specified relative to the directory in which it is installed so that
# it will resolve properly within chrooted installations.
%global script 'use File::Spec; print File::Spec->abs2rel($ARGV[0], $ARGV[1])'
%global abs2rel perl -e %{script}
# Standard JPackage naming and versioning defines.
%global priority        17147
%global javaver         1.7.0
%global buildver        65
# Standard JPackage directories and symbolic links.
%global sdklnk          java-%{javaver}-openjdk
%global archname        %{sdklnk}
%global jrelnk          jre-%{javaver}-openjdk
%global sdkdir          %{sdklnk}-%{javaver}
%global jredir          %{sdkdir}/jre
%global sdkbindir       %{_jvmdir}/%{sdklnk}/bin
%global jrebindir       %{_jvmdir}/%{jrelnk}/bin
%global jvmjardir       %{_jvmjardir}/%{sdkdir}
%global jvmjarlink      %{_jvmjardir}/%{sdklnk}
# Prevent brp-java-repack-jars from being run.
%global __jar_repack 0
# cacert symlink
%global cacerts  %{_jvmdir}/%{jredir}/lib/security/cacerts
# real file made by update-ca-certificates
%global javacacerts %{_var}/lib/ca-certificates/java-cacerts
%global with_default_hotspot_tarball 1
%ifarch %aarch64
%global _with_bootstrap 1
%global _with_zero 1
%endif
# turn zero on non jit arches by default
%ifnarch %{jit_arches}
%global _with_zero 1
%endif
%bcond_with zero
%bcond_without bootstrap
%if %{with zero}
%define something 1
%endif

%changelog
