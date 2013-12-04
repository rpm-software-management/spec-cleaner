
Name: multilinedefine
%define postInstall() \
. %{_sysconfdir}/selinux/config; \
if [ -e /etc/selinux/%2/.rebuild ]; then \
   rm /etc/selinux/%2/.rebuild; \
   (cd /etc/selinux/%2/modules/active/modules; rm -f shutdown.pp amavis.pp clamav.pp gnomeclock.pp matahari.pp xfs.pp kudzu.pp kerneloops.pp execmem.pp openoffice.pp ada.pp tzdata.pp hal.pp hotplug.pp howl.pp java.pp mono.pp moilscanner.pp gamin.pp audio_entropy.pp audioentropy.pp iscsid.pp polkit_auth.pp polkit.pp rtkit_daemon.pp ModemManager.pp telepathysofiasip.pp ethereal.pp passanger.pp qpidd.pp pyzor.pp razor.pp pki-selinux.pp phpfpm.pp consoletype.pp ctdbd.pp fcoemon.pp isnsd.pp l2tp.pp rgmanager.pp corosync.pp aisexec.pp pacemaker.pp ) \
   /usr/sbin/semodule -B -n -s %2; \
else \
    touch /etc/selinux/%2/modules/active/modules/sandbox.disabled \
fi; \
if [ "${SELINUXTYPE}" == "%2" ]; then \
   if selinuxenabled; then \
      load_policy; \
   else \
      # selinux isn't enabled \
      # (probably a first install of the policy) \
      # -> we can't load the policy \
      true; \
   fi; \
fi; \
if selinuxenabled; then \
   if [ %1 -eq 1 ]; then \
      /sbin/restorecon -R /root /var/log /var/run 2> /dev/null; \
   else \
      %relabel %2 \
   fi; \
else \
   # run fixfiles on next boot \
   touch /.autorelabel \
fi;
