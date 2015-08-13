%package guest-KMP
Summary:        Guest kernel modules for VirtualBox
Group:          System/Emulators/PC
#SUSE specify macro to define guest kmp package                                
%{?suse_kernel_module_package:%{suse_kernel_module_package} -p %{SOURCE8} -n %{name}-guest -f %{SOURCE6} kdump um xen xenpae}
%kernel_module_package -p %{name}-kmp-preamble
