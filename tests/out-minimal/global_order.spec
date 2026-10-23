# Test for issue #239: %global lines referencing macros defined by the
# preamble tags must not be hoisted above those tags as %global expands
# its value immediately.
%define _plain_define 1
Name:           globalorder
Version:        1.0.5
Release:        0
# Full Plasma 5 version (e.g. 5.8.95)
%{!?_plasma5_bugfix: %global _plasma5_bugfix %{version}}
# Lasted ABI-stable Plasma (e.g. 5.8 in KF5, but 5.8.95 in KUF)
%{!?_plasma5_version: %global _plasma5_version %(echo %{_plasma5_bugfix} | awk -F. '{print $1"."$2}')}
%global _suffixed %{name}-suffix
Summary:        Global evaluation order
License:        MIT
Requires:       foo = %{_plasma5_version}

%description
Check that spec-cleaner does not hoist version-dependent globals above Version:.

%changelog
