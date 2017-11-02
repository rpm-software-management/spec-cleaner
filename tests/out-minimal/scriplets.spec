%post -n %libname -p /sbin/ldconfig

%post
/sbin/ldconfig

%post
/sbin/ldconfig
someothercommand

%post -n %{_libname}
/sbin/ldconfig

%filetriggerin tools -- %{_datadir}/icons
if [ "$(realpath %{_bindir}/gtk-update-icon-cache)" = "%{_bindir}/gtk-update-icon-cache-2.0" ]; then
  for ICON_THEME in $(cut -d / -f 5 | sort -u); do
    if [ -f "%{_datadir}/icons/${ICON_THEME}/index.theme" ]; then
      %{_bindir}/gtk-update-icon-cache --quiet --force "%{_datadir}/icons/${ICON_THEME}"
    fi
  done
fi

%filetriggerpostun tools -- %{_datadir}/icons
if [ "$(realpath %{_bindir}/gtk-update-icon-cache)" = "%{_bindir}/gtk-update-icon-cache-2.0" ]; then
  for ICON_THEME in $(cut -d / -f 5 | sort -u); do
    if [ -f "%{_datadir}/icons/${ICON_THEME}/index.theme" ]; then
      %{_bindir}/gtk-update-icon-cache --quiet --force "%{_datadir}/icons/${ICON_THEME}"
    fi
  done
fi

%changelog
