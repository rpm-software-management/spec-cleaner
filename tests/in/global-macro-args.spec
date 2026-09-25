%global global_macro() echo 'global macro used with arg %1'
%define  spaced_macro() echo 'spaced macro used with arg %1'

%build
%global_macro 15
%spaced_macro 16
