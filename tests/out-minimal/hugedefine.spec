%description sdk-doc
Bla bla bla

%define langpack(c:Ei:L:l:Mm:n:p:r:S:s:TXx:) \
%define project LibreOffice \
%define lang %{-l:%{-l*}}%{!-l:%{error:Language code not defined}} \
%define _langpack_lang %{-L:%{-L*}}%{!-L:%{lang}} \
%define pkgname l10n-%{lang} \
%define langname %{-n:%{-n*}}%{!-n:%{error:Language name not defined}} \
\
%global langpack_langs %{langpack_langs} %{_langpack_lang} %{-i:%{-i*}} \
\
%package %{pkgname} \
Summary:        %{langname} Localization Files for LibreOffice \
Group:          Productivity/Office/Suite \
Requires:       %{name} = %{version} \
Provides:       locale(libreoffice:%{lang}) \
%if %{with noarch_subpkgs} \
Requires(post,): %{name} = %{version} \
Requires(postun,): %{name} = %{version} \
BuildArch:      noarch \
%endif \
%{-m:Requires: myspell-%{-m*}}%{!-m:%{-M:Requires: myspell-%{lang}}} \
%{-r:Requires: %{-r*}} \
%{-p:Provides: %{name}-l10n-%{-p*}} \
%{-T: \
Provides:       %{name}-help-%{lang} = %{version} \
Obsoletes:      %{name}-help-%{lang} < %{version} \
%{-L: \
Provides:       %{name}-help-%{-L*} = %{version} \
Obsoletes:      %{name}-help-%{-L*} < %{version} \
} \
%{-p: \
Provides:       %{name}-help-%{-p*} = %{version} \
Obsoletes:      %{name}-help-%{-p*} < %{version} \
} \
} \
\
%description %{pkgname} \
Provides additional %{langname} translations and resources for %{project}. \
\
%files %{pkgname} \
%defattr(-,root,root) \
%{!-E: \
%define autotextdir %{_datadir}/%{name}/share/autotext \
%{expand:%%_langpack_common %{_langpack_lang}} \
%{-x:%{autotextdir}/%{-x*}}%{!-x:%{-X:%{autotextdir}/%{_langpack_lang}}} \
%{-c:%{_datadir}/%{name}/share/registry/%{-c*}.xcd} \
%{-s:%{_datadir}/%{name}/share/registry/%{-s*}_%{_langpack_lang}.xcd} \
%{-T: \
%docdir %{_datadir}/%{name}/help/%{_langpack_lang} \
%{_datadir}/%{name}/help/%{_langpack_lang} \
} \
%{-i:%{expand:%%_langpack_common %{-i*}}} \
} \
%{nil}
%define _link_noarch_files() \
%posttrans %{1} \
rpm -ql %{name}-%{1} > %{_datadir}/libreoffice/%{1}_list.txt || true \
if [ -f %{_datadir}/libreoffice/%{1}_list.txt ] ; then \
    %{_datadir}/libreoffice/link-to-ooo-home %{_datadir}/libreoffice/%{1}_list.txt || true \
fi \
\
%postun %{1} \
if [ "$1" = "0" -a -f %{_datadir}/libreoffice/%{1}_list.txt -a -f
%{_datadir}/libreoffice/link-to-ooo-home ]; then \
    %{_datadir}/libreoffice/link-to-ooo-home --unlink %{_datadir}/libreoffice/%{1}_list.txt || true \
    rm -f %{_datadir}/libreoffice/%{1}_list.txt 2> /dev/null || true \
fi \
%{nil}

%changelog
