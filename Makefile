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

check: spec-cleaner pkgconfig_conversions.txt licenses_changes.txt
	@echo "Running tests:"; \
	for i in tests/in/*.spec; do \
		CORRECT="`echo $$i | sed 's|^tests/in|tests/out|'`" ;\
		NEW="`    echo $$i | sed 's|^tests/in|tests/tmp|'`" ;\
		TEST="`   echo $$i | sed 's|^tests/in/\(.*\).spec|\1|'`" ;\
		spec-cleaner -f $$i -o "$$NEW"; \
		echo -n " * test '$$TEST': ";\
		if [ "`diff "$$CORRECT" "$$NEW"`" ]; then \
			echo "failed" ;\
			FAILED="$$FAILED $$TEST" ;\
		else\
			echo "passed" ;\
		fi ;\
	done ;\
	echo ;\
	if [ "$$FAILED" ]; then \
		echo "These `echo $$FAILED | wc -w` tests out of `echo tests/in/*.spec | wc -w` failed:" ;\
		echo "  $$FAILED" ;\
		echo ;\
		exit 1 ;\
	else \
		echo "All tests passed!" ;\
		echo ;\
	fi

clean:
	rm -rf tests/tmp/*

.PHONY: install check test
