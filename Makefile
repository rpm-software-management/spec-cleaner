all: pkgconfig_conversions.txt

pkgconfig_conversions.txt: pkgconfig-update.sed pkgconfig-update.sh 
	sh pkgconfig-update.sh 13.1 > $@

install: pkgconfig_conversions.txt licenses_changes.txt spec-cleaner
	install -d $(DESTDIR)/usr/bin/ ; \
	install -m 755 spec-cleaner $(DESTDIR)/usr/bin
	install -d $(DESTDIR)/usr/share/spec-cleaner/ ; \
	install -m 644 licenses_changes.txt $(DESTDIR)/usr/share/spec-cleaner/ ; \
	install -m 644 pkgconfig_conversions.txt $(DESTDIR)/usr/share/spec-cleaner/

test: check

check:
	echo "true"

.PHONY: install check test upkg
