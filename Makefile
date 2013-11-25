PREFIX ?= /usr
BINDIR ?= $(PREFIX)/bin
DATADIR ?= $(PREFIX)/share
LIBEXECDIR ?= $(PREFIX)/libexec
LIBDIR ?= $(PREFIX)/lib
SITEDIR ?= $(LIBDIR)/python2.7/site-packages

all: data/pkgconfig_conversions.txt data/licenses_changes.txt

data/pkgconfig_conversions.txt: pkgconfig-update.sed pkgconfig-update.sh
	@sh pkgconfig-update.sh 13.1 > $@

data/licenses_changes.txt: license-update.sh
	@sh license-update.sh > $@

install: bin/spec-cleaner
	@echo "Installing package to $(DESTDIR)" ; \
	install -d $(DESTDIR)$(BINDIR) ; \
	install -m 755 bin/spec-cleaner $(DESTDIR)/$(BINDIR)
	@install -d $(DESTDIR)$(DATADIR)/spec-cleaner/ ; \
	install -m 644 data/licenses_changes.txt $(DESTDIR)$(DATADIR)/spec-cleaner/ ; \
	install -m 644 data/pkgconfig_conversions.txt $(DESTDIR)$(DATADIR)/spec-cleaner/ ; \
	install -m 644 data/excludes-bracketing.txt $(DESTDIR)$(DATADIR)/spec-cleaner/
	@install -d $(DESTDIR)$(LIBEXECDIR)/obs/service/ ; \
	install -m 755 obs/format_spec_file $(DESTDIR)$(LIBEXECDIR)/obs/service/ ; \
	install -m 644 obs/format_spec_file.service $(DESTDIR)$(LIBEXECDIR)/obs/service/
	@install -d $(DESTDIR)$(SITEDIR)/spec_cleaner ; \
	install -m 755 spec_cleaner/__init__.py  $(DESTDIR)$(SITEDIR)/spec_cleaner/ ; \
	install -m 644 spec_cleaner/rpmcleaner.py  $(DESTDIR)$(SITEDIR)/spec_cleaner/ ; \
	install -m 644 spec_cleaner/rpmcopyright.py $(DESTDIR)$(SITEDIR)/spec_cleaner/ ; \
	install -m 644 spec_cleaner/rpmexception.py  $(DESTDIR)$(SITEDIR)/spec_cleaner/ ; \
	install -m 644 spec_cleaner/rpmsection.py $(DESTDIR)$(SITEDIR)/spec_cleaner/ ; \
	install -m 644 spec_cleaner/fileutils.py $(DESTDIR)$(SITEDIR)/spec_cleaner/ ; \
	install -m 644 spec_cleaner/rpmbuild.py $(DESTDIR)$(SITEDIR)/spec_cleaner/ ; \
	install -m 644 spec_cleaner/rpmdescription.py $(DESTDIR)$(SITEDIR)/spec_cleaner/ ; \
	install -m 644 spec_cleaner/rpmfiles.py $(DESTDIR)$(SITEDIR)/spec_cleaner/ ; \
	install -m 644 spec_cleaner/rpminstall.py $(DESTDIR)$(SITEDIR)/spec_cleaner/ ; \
	install -m 644 spec_cleaner/rpmpreamble.py $(DESTDIR)$(SITEDIR)/spec_cleaner/ ; \
	install -m 644 spec_cleaner/rpmprep.py $(DESTDIR)$(SITEDIR)/spec_cleaner/ ; \
	install -m 644 spec_cleaner/rpmprune.py $(DESTDIR)$(SITEDIR)/spec_cleaner/ ; \
	install -m 644 spec_cleaner/rpmscriplets.py $(DESTDIR)$(SITEDIR)/spec_cleaner/ ; \
	install -m 644 spec_cleaner/rpmregexp.py $(DESTDIR)$(SITEDIR)/spec_cleaner/ ; \
	install -m 644 spec_cleaner/rpmcheck.py $(DESTDIR)$(SITEDIR)/spec_cleaner/

test: check

check: spec_cleaner/__init__.py
	@echo "Running tests in python2:" ; \
	for i in tests/in/*.spec; do \
		CORRECT="`echo $$i | sed 's|^tests/in|tests/out|'`" ; \
		NEW="`    echo $$i | sed 's|^tests/in|tests/tmp|'`" ; \
		TEST="`   echo $$i | sed 's|^tests/in/\(.*\).spec|\1|'`" ; \
		python2 spec_cleaner/__init__.py -p -f $$i | sed "s|`date +%%Y`|2013|" > "$$NEW" ; \
		echo -n " * test '$$TEST': " ; \
		if [ "`diff "$$CORRECT" "$$NEW" 2>&1`" ]; then \
			echo "failed" ; \
			FAILED="$$FAILED $$TEST" ; \
		else \
			echo "passed" ; \
		fi ; \
	done ; \
	if [ -x /usr/bin/python3 ]; then \
		echo "Running tests in python3:" ; \
		for i in tests/in/*.spec; do \
			CORRECT="`echo $$i | sed 's|^tests/in|tests/out|'`" ; \
			NEW="`    echo $$i | sed 's|^tests/in|tests/tmp|'`" ; \
			TEST="`   echo $$i | sed 's|^tests/in/\(.*\).spec|\1|'`" ; \
			python3 spec_cleaner/__init__.py -p -f $$i | sed "s|`date +%%Y`|2013|" > "$$NEW" ; \
			echo -n " * test '$$TEST': " ; \
			if [ "`diff "$$CORRECT" "$$NEW" 2>&1`" ]; then \
				echo "failed" ; \
				FAILED="$$FAILED $$TEST" ; \
			else \
				echo "passed" ; \
			fi ; \
		done ; \
	fi ; \
	echo ; \
	if [ "$$FAILED" ]; then \
		echo "`echo $$FAILED | wc -w` tests out of `echo tests/in/*.spec | wc -w` failed:" ; \
		echo "  $$FAILED" ; \
		echo ; \
		echo "Check errors by running:"; \
		for i in $$FAILED; do echo "  diff -Naru tests/out/$$i.spec tests/tmp/$$i.spec"; done; \
		echo ; \
		exit 1 ; \
	else \
		echo "All tests passed!" ; \
		echo ; \
	fi

clean:
	rm -rf tests/tmp/* \
	rm -rf spec_cleaner/*.pyc

.PHONY: install check test clean
